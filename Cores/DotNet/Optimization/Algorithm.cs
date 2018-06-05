using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
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

        public List<Func<object, JObject>> writers = new List<Func<object, JObject>>();

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

        public TV Work(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area, string logStates = null)
        {
            var logger = new Logger<TBase, TFuncType, TV>(logStates, writers);
            logger.Initialize();
            
            Initialize(f, area);
            logger.Log(State, CurrentNode);
            bool continueOrNot = true;
            while (continueOrNot)
            {
                CurrentNode.Process(f, area, State);
                logger.Log(State, CurrentNode);
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
            logger.Log(State, CurrentNode);
            return State.result;
        }

        public JObject SerializeState() => this.State.ConvertToJson(writers);
    }

    public class Logger<TBase, TFuncType, TV> where TV : class, IOptimizable<TBase, TFuncType>
    {
        public int Counter = 1;

        public string LogLocation;
        public List<Func<object, JObject>> Writers;

        public Logger(string logLocation, List<Func<Object, JObject>> writers)
        {
            this.LogLocation = logLocation;
            this.Writers = writers;
        }

        public void PurgeFolder(DirectoryInfo dir)
        {
            foreach (FileInfo f in dir.GetFiles()) f.Delete();
            foreach (DirectoryInfo sd in dir.GetDirectories()) sd.Delete(true);
        }

        public void Initialize()
        {
            if (LogLocation != null)
            {
                var dir = new DirectoryInfo(LogLocation);
                if (dir.Exists)
                    PurgeFolder(dir);
                else
                    dir.Create();
            }
        }

        public void Log(State<TBase, TFuncType, TV> state, GeneralNode<TBase, TFuncType, TV> node)
        {
            if (LogLocation != null)
            {
                state.SetParameter("_nodeId", node.NodeId);
                var printer = new StreamWriter($"{LogLocation}/{Counter}.json");
                printer.WriteLine(state.ConvertToJson(Writers).ToString(Formatting.Indented));
                printer.Close();
                printer.Dispose();
                ++Counter;
            }
        }

    }
}