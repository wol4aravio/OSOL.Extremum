using System;
using System.Collections.Generic;
using System.IO;
using CommandLine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions;

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
    
            [Option('f', "field", Required = true, HelpText = "Target field")]
            public string Field { get; set; }
            
            [Option('r', "result", Required = true, HelpText = "Where to save the result")]
            public string ResultFile { get; set; }
        }

        static void Body(Options opts)
        {
            var algConfig = JObject.Parse(File.ReadAllText(opts.AlgorithmConfig));
            var language = algConfig["language"].Value<string>();
            var name = algConfig["algorithm"].Value<string>();
            
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
                f.Initialize();
                var result = algorithm.Work(x => f.Calculate(x), area);
                f.Terminate();

                using (StreamWriter sw = new StreamWriter(opts.ResultFile))
                using (JsonWriter writer = new JsonTextWriter(sw){ Formatting = Formatting.Indented })
                {
                    result.ConvertToJson().WriteTo(writer);
                }
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