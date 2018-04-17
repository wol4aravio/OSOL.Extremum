using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using Newtonsoft.Json.Linq;
using OSOL.Extremum.Core.DotNet.Arithmetics;
using OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser.Trees;

namespace OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser
{
    public static class Parser
    {
        public class UnsupportedOperation: Exception {}
        
        private static FileStream ExtractResource(string filename, string suffix, string location = "", string where = ".")
        {
            var assembly = Assembly.GetExecutingAssembly();
            string resourceName = $"OSOL.Extremum.Core.DotNet.Resources.{filename}.{suffix}";
            if(location.Length != 0)
            {
                resourceName = $"OSOL.Extremum.Core.DotNet.Resources.{location}.{filename}.{suffix}";
            }
            var resource = assembly.GetManifestResourceStream(resourceName);

            if (!Directory.Exists(where))
            {
                Directory.CreateDirectory(where);
            }

            var file = File.Create($"{where}/{filename}.{suffix}");
            resource.CopyTo(file);
            file.Close();

            return file;
        }
        
        public static JObject ParseString(string str)
        {
            var rootFolder = "temp";
            var parserLibFile = ExtractResource("parser", "py", "parser", $"{rootFolder}/parser");
            var parserLibInitFile = ExtractResource("__init__", "py", "parser", $"{rootFolder}/parser");
            var parserAppFile = ExtractResource("parser_app", "py", "apps", rootFolder);
            
            
            
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "python";
            start.Arguments = $"{parserAppFile.Name} --function \"{str}\"";
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd().Replace('\'', '\"');
                    
                    Directory.Delete(rootFolder, true);
                    return JObject.Parse(result);
                }
            }
        }

        public static Tree<double> BuildTreeD(JObject json)
        {
            switch (json["type"].Value<string>())
            {
                case "binary":
                {
                    var op = json["op"].Value<string>();
                    var leftTree = BuildTreeD((JObject)json["left"]);
                    var rightTree = BuildTreeD((JObject)json["right"]);
                    switch (op)
                    {
                        case "add": return new TreeD.AdditionTree(leftTree, rightTree);
                        case "sub": return new TreeD.SubtractionTree(leftTree, rightTree);
                        case "mult": return new TreeD.MultiplicationTree(leftTree, rightTree);
                        case "div": return new TreeD.DivisionTree(leftTree, rightTree);
                        case "pow": return new TreeD.PowerTree(leftTree, rightTree);
                        default: throw new UnsupportedOperation();
                    }
                    break;
                }
                case "unary":
                {
                    var op = json["op"].Value<string>();
                    var operandTree = BuildTreeD((JObject)json["operand"]);
                    switch (op)
                    {
                        case "usub": return new TreeD.NegTree(operandTree);
                        default: throw new UnsupportedOperation();
                    }
                    break;
                }
                case "func":
                {
                    var op = json["func"].Value<string>();
                    var argsTrees = BuildTreeD((JObject)((JArray)json["args"])[0]);
                    switch (op)
                    {
                        case "sin": return new TreeD.SinTree(argsTrees);
                        case "cos": return new TreeD.CosTree(argsTrees);
                        case "exp": return new TreeD.ExpTree(argsTrees);
                        case "abs": return new TreeD.AbsTree(argsTrees);
                        case "ln": return new TreeD.LnTree(argsTrees);
                        case "sqrt": return new TreeD.SqrtTree(argsTrees);
                        default: throw new UnsupportedOperation();
                    }
                    break;
                }
                case "const": return new TreeD.ConstantTree(json["value"].Value<double>());
                case "var": return new TreeD.VariableTree(json["name"].Value<string>());
                default: throw new SerializationException();
            }
        }
        
        public static Tree<Interval> BuildTreeI(JObject json)
        {
            switch (json["type"].Value<string>())
            {
                case "binary":
                {
                    var op = json["op"].Value<string>();
                    var leftTree = BuildTreeI((JObject)json["left"]);
                    var rightTree = BuildTreeI((JObject)json["right"]);
                    switch (op)
                    {
                        case "add": return new TreeI.AdditionTree(leftTree, rightTree);
                        case "sub": return new TreeI.SubtractionTree(leftTree, rightTree);
                        case "mult": return new TreeI.MultiplicationTree(leftTree, rightTree);
                        case "div": return new TreeI.DivisionTree(leftTree, rightTree);
                        case "pow": return new TreeI.PowerTree(leftTree, rightTree);
                        default: throw new UnsupportedOperation();
                    }
                    break;
                }
                case "unary":
                {
                    var op = json["op"].Value<string>();
                    var operandTree = BuildTreeI((JObject)json["operand"]);
                    switch (op)
                    {
                        case "usub": return new TreeI.NegTree(operandTree);
                        default: throw new UnsupportedOperation();
                    }
                    break;
                }
                case "func":
                {
                    var op = json["func"].Value<string>();
                    var argsTrees = BuildTreeI((JObject)((JArray)json["args"])[0]);
                    switch (op)
                    {
                        case "sin": return new TreeI.SinTree(argsTrees);
                        case "cos": return new TreeI.CosTree(argsTrees);
                        case "exp": return new TreeI.ExpTree(argsTrees);
                        case "abs": return new TreeI.AbsTree(argsTrees);
                        case "ln": return new TreeI.LnTree(argsTrees);
                        case "sqrt": return new TreeI.SqrtTree(argsTrees);
                        default: throw new UnsupportedOperation();
                    }
                    break;
                }
                case "const": return new TreeI.ConstantTree(json["value"].Value<double>());
                case "var": return new TreeI.VariableTree(json["name"].Value<string>());
                default: throw new SerializationException();
            }
        }
    }
}