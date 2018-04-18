using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json.Linq;
using OSOL.Extremum.Cores.DotNet.Optimization.Nodes;

namespace OSOL.Extremum.Cores.DotNet.Optimization
{

    using Area = Dictionary<string, Tuple<double, double>>;

    public class Algorithm<TBase, TFuncType, TV> where TV : class, IOptimizable<TBase, TFuncType>
    {
        public State<TBase, TFuncType, TV> State = new State<TBase, TFuncType, TV>();
        public GeneralNode<TBase, TFuncType, TV> CurrentNode = null;

        public GeneralNode<TBase, TFuncType, TV>[] Nodes;
        public Tuple<int, int?, int>[] TransitionMatrix;

        public Algorithm(GeneralNode<TBase, TFuncType, TV>[] nodes, Tuple<int, int?, int>[] transitionMatrix)
        {
            this.Nodes = nodes;
            this.TransitionMatrix = transitionMatrix;
        }

        public void Initialize(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area)
        {
            foreach (var n in Nodes)
            {
                n.Initialize(f, area, State);
            }

            CurrentNode = Nodes.First();
        }

        public void Reset()
        {
            this.State = new State<TBase, TFuncType, TV>();
            this.CurrentNode = null;
        }

        public TV Work(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area)
        {
            Initialize(f, area);
            bool continueOrNot = true;
            while (continueOrNot)
            {
                CurrentNode.Process(f, area, State);
                var currentConditionValue = CurrentNode.GetCurrentCondition(f, area, State);
                var nextNodes = TransitionMatrix
                    .Where(rule => rule.Item1 == CurrentNode.NodeId && rule.Item2 == currentConditionValue)
                    .Select(rule => (double) rule.Item3).ToArray();
                var nextNode = nextNodes.Length == 0 ? double.NaN : nextNodes[0];
                if (double.IsNaN(nextNode))
                {
                    continueOrNot = false;
                }
                else
                {
                    CurrentNode = Nodes.First(n => n.NodeId == (int) nextNode);
                }
            }

            return State.result;
        }

        public JObject SerializeState() => this.State.ConvertToJson();
    }
}