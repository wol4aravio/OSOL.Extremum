using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using Newtonsoft.Json.Linq;

namespace OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser
{
    public static class Parser
    {
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
        
        public static object ParseString(string str)
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
                    string result = reader.ReadToEnd();
                    
                    Directory.Delete(rootFolder, true);
                    return result;
                }
            }
            
        }
    }
}