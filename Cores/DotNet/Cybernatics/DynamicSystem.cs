using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Cores.DotNet.Vectors;

namespace OSOL.Extremum.Cores.DotNet.Cybernatics
{
    public abstract class DynamicSystem<TBase>
    {
        public Func<VectorObject<TBase>, VectorObject<TBase>> f, u;
        public ButcherTableau butcherTableau;

        public abstract TBase DoubleToBase(double d);
        public abstract double BaseToDouble(TBase b);

        public VectorObject<TBase> Prolong(double currentTime, VectorObject<TBase> currentState,
            VectorObject<TBase> controls, double eps)
        {
            Dictionary<int, VectorObject<TBase>> kElements = new Dictionary<int, VectorObject<TBase>>();
            kElements.Add(
                1,
                f(currentState
                    .Union(Tuple.Create("t", DoubleToBase(currentTime)))
                    .Union(controls.Elements.Select(kvp => Tuple.Create(kvp.Key, kvp.Value)).ToArray()))
            );
            for (var i = 2; i <= butcherTableau.numberOfParts; ++i)
            {
                var newTime = DoubleToBase(currentTime + eps * butcherTableau.GetC(i));
                var products = new List<VectorObject<TBase>>();
                for (int j = 1; j < i; ++j)
                    products.Add(kElements[j] * butcherTableau.GetA(i, j));
                var newState = currentState + products.Skip(1).Aggregate(products.First(), (acc, v) => acc + v) * eps;
                var newK = f(newState
                    .Union(Tuple.Create("t", newTime))
                    .Union(controls.Elements.Select(kvp => Tuple.Create(kvp.Key, kvp.Value)).ToArray())
                );
                kElements.Add(i, newK);
            }

            var kProducts = new List<VectorObject<TBase>>();
            for (int i = 1; i <= butcherTableau.numberOfParts; ++i)
                kProducts.Add(kElements[i] * butcherTableau.GetB(i));
            return currentState + kProducts.Skip(1).Aggregate(kProducts.First(), (acc, v) => acc + v) * eps;
        }

        public Tuple<List<double>, List<VectorObject<TBase>>, List<VectorObject<TBase>>> Simulate(
            VectorObject<TBase> initialCondition, double eps, Dictionary<string, Tuple<double, double>> terminationConditions,
            int maxSteps, double maxOverallError)
        {
            var stop = false;
            var times = new List<double>() {0.0};
            var states = new List<VectorObject<TBase>>() {initialCondition};
            var controls = new List<VectorObject<TBase>>();
            for (int stepId = 1; stepId <= maxSteps && !stop; ++stepId)
            {
                var currentTime = times.Last();
                var currentState = states.Last();
                var control = u(currentState.Union(Tuple.Create("t", DoubleToBase(currentTime))));
                var newState = Prolong(currentTime, currentState, control, eps);
                var newTime = DoubleToBase(eps * stepId);
                var terminalConditionError = newState
                    .Union(Tuple.Create("t", newTime))
                    .Union(control.Elements.Select(kvp => Tuple.Create(kvp.Key, kvp.Value)).ToArray())
                    .DistanceFromArea(terminationConditions);
                stop = terminalConditionError.Select(kvp => kvp.Value).Sum() <= maxOverallError;
                times.Add(BaseToDouble(newTime));
                states.Add(newState);
                controls.Add(control);
            }

            return Tuple.Create(times, states, controls);
        }

    }
}