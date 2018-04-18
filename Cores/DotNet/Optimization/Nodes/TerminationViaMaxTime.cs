using System;
using System.Collections.Generic;

namespace OSOL.Extremum.Cores.DotNet.Optimization.Nodes
{

    using Area = Dictionary<string, Tuple<double, double>>;

    public class TerminationViaMaxTime<TBase, TFuncType, TV> : GeneralNode<TBase, TFuncType, TV>
        where TV : class, IOptimizable<TBase, TFuncType>
    {
        private readonly string ParameterName;
        private readonly double MaxTime;

        public TerminationViaMaxTime(int nodeId, double maxTime, string parameterName = "startTime")
        {
            this.NodeId = nodeId;
            this.MaxTime = maxTime;
            this.ParameterName = parameterName;
        }

        public override void Initialize(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area,
            State<TBase, TFuncType, TV> state)
        {
            DateTime? value = null;
            try
            {
                value = state.GetParameter<DateTime>(ParameterName);
            }
            catch (OptimizationExceptions.NoSuchParameterException e)
            {
                state.SetParameter<DateTime>(name: ParameterName, value: DateTime.Now);
            }
            finally
            {
                if (value.HasValue)
                {
                    throw new OptimizationExceptions.ParameterAlreadyExistsException(ParameterName);
                }
            }
        }

        public override void Process(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area,
            State<TBase, TFuncType, TV> state)
        {
        }

        public override int? GetCurrentCondition(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area,
            State<TBase, TFuncType, TV> state) =>
            (DateTime.Now - state.GetParameter<DateTime>(ParameterName)).TotalSeconds > MaxTime ? 1 : 0;

    }
}