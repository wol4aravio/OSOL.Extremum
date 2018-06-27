using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using CommandLine;
using CSharpx;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using OSOL.Extremum.Cores.DotNet.Optimization;
using OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions;
using OSOL.Extremum.Cores.DotNet.Vectors;

namespace OSOL.Extremum.Apps.DotNet
{
    class Program
    {
        
        class Options {
            [Option('a', "algorithm", Required = true, HelpText = "Algorithm config file")]
            public string AlgorithmConfig { get; set; }
    
            [Option('t', "task", Required = true, HelpText = "Task config file")]
            public string TaskConfig { get; set; }
    
            [Option('p', "port", Required = true, HelpText = "Port where to run server")]
            public int Port { get; set; }
    
            [Option('f', "field", Default = "target", HelpText = "Target field")]
            public string Field { get; set; }
            
            [Option('r', "result", Required = true, HelpText = "Where to save the result")]
            public string ResultFile { get; set; }
            
            [Option('o', "output", Default = "json", HelpText = "Output form")]
            public string OutputForm { get; set; }
            
            [Option('l', "logStates", Default = "_none", HelpText = "Log states")]
            public string LogStates { get; set; }
        }

        static RealVector RunRealVectorAlgorithm(
            Algorithm<RealVector, double, RealVector> algorithm, 
            RealRemoteFunction f, 
            Dictionary<string, Tuple<double, double>> area, string logStates)
        {
            f.Initialize();
            var result = algorithm.Work(x => f.Calculate(x), area, logStates);
            f.Terminate();
            return result;
        }

        static void SaveRealVectorResult(RealVector result, Options opts)
        {
            if (string.Equals(opts.OutputForm, "json"))
            {
                using (StreamWriter sw = new StreamWriter(opts.ResultFile + ".json"))
                using (JsonWriter writer = new JsonTextWriter(sw) {Formatting = Formatting.Indented})
                {
                    result.ConvertToJson().WriteTo(writer);
                }
            }

            if (string.Equals(opts.OutputForm, "csv"))
            {
                using (StreamWriter sw = new StreamWriter(opts.ResultFile + ".csv"))
                {
                    sw.WriteLine(String.Join(",", result.Elements.Select(kvp => kvp.Key)));
                    sw.WriteLine(String.Join(",", result.Elements.Select(kvp => kvp.Value)));
                }
            }
        }

        static void Body(Options opts)
        {
            var algConfig = JObject.Parse(File.ReadAllText(opts.AlgorithmConfig));
            var language = algConfig["language"].Value<string>();
            var name = algConfig["algorithm"].Value<string>();
            var logStates = opts.LogStates;
            if (string.Equals(logStates, "_none"))
                logStates = null;
            
            var taskConfig = JObject.Parse(File.ReadAllText(opts.TaskConfig));
            var area = new Dictionary<string, Tuple<Double, Double>>();
            foreach (var areaPart in taskConfig["area"])
            {
                area.Add(
                    areaPart["name"].Value<string>(), 
                    Tuple.Create(areaPart["min"].Value<double>(), areaPart["max"].Value<double>()));
            }
            
            if (string.Equals(language, "CSharp") && (string.Equals(name, "RS") || string.Equals(name, "RandomSearch")))
            {
                var radius = algConfig["radius"].Value<double>();
                var maxTime = algConfig["maxTime"].Value<double>();
                var algorithm = Algorithms.CSharp.RandomSearch.CreateFixedStepRandomSearch(radius, maxTime);
                
                var f = new RealRemoteFunction(opts.TaskConfig, opts.Port, opts.Field);
                var result = RunRealVectorAlgorithm(algorithm, f, area, logStates);
                
                SaveRealVectorResult(result, opts);
                return;
            }

            if (string.Equals(language, "FSharp") && (string.Equals(name, "RS") || string.Equals(name, "RandomSearch")))
            {
                var radius = algConfig["radius"].Value<double>();
                var maxTime = algConfig["maxTime"].Value<double>();
                var algorithm = Algorithms.FSharp.RandomSearch.CreateFixedStepRandomSearch(radius, maxTime);
                
                var f = new RealRemoteFunction(opts.TaskConfig, opts.Port, opts.Field);
                var result = RunRealVectorAlgorithm(algorithm, f, area, logStates);

                SaveRealVectorResult(result, opts);
                return;
            }

            if (string.Equals(language, "CSharp") && (string.Equals(name, "DE") || string.Equals(name, "DifferentialEvolution")))
            {
                var populationSize = algConfig["populationSize"].Value<int>();
                var weightingFactor = algConfig["weightingFactor"].Value<double>();
                var crossoverRate = algConfig["crossoverRate"].Value<double>();
                var maxTime = algConfig["maxTime"].Value<double>();
                var algorithm = Algorithms.CSharp.DifferentialEvolution.CreateDifferentialEvolution(populationSize, weightingFactor, crossoverRate, maxTime);
                
                var f = new RealRemoteFunction(opts.TaskConfig, opts.Port, opts.Field);
                var result = RunRealVectorAlgorithm(algorithm, f, area, logStates);
                
                SaveRealVectorResult(result, opts);
                return;
            }

            throw new Exception("Unsupported Algorithm");
        }
        
        static void Main(string[] args)
        {
            CommandLine.Parser.Default.ParseArguments<Options>(args).WithParsed(opts => Body(opts));
        }
    }
}