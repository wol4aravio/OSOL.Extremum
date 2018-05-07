using System.Collections.Generic;
using System.Diagnostics;
using System.Net;

namespace OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions
{
    public abstract class RemoteFunction<TFuncType>
    {
        public string Json;
        public int Port;
        public string Field;
        public Process ServerProcess;
        public WebClient Client = new WebClient();

        protected RemoteFunction(string json, int port, string field)
        {
            this.Json = json;
            this.Port = port;
            this.Field = field;
            
            ProcessStartInfo scriptConfig = new ProcessStartInfo();
            scriptConfig.FileName = "run_core";
            scriptConfig.Arguments = $"--core {this.Json} --port {this.Port}";
            scriptConfig.UseShellExecute = false;
            this.ServerProcess = Process.Start(scriptConfig);
            System.Threading.Thread.Sleep(5000);
        }

        public abstract TFuncType Calculate(Dictionary<string, TFuncType> values);

        public void Terminate()
        {
            ServerProcess.Kill();
        }
    }
}