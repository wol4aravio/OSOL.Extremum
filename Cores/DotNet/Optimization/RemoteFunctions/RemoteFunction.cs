using System.Collections.Generic;
using System.Diagnostics;
using System.Net;
using System.Net.Cache;
using System.Net.Http;

namespace OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions
{
    public abstract class RemoteFunction<TFuncType>
    {
        public string Json;
        public int Port;
        public string Field;
        private ProcessStartInfo ScriptConfig;
        public Process ServerProcess;
        public WebClient Client = new WebClient();

        protected RemoteFunction(string json, int port, string field)
        {                
            this.Json = json;
            this.Port = port;
            this.Field = field;
            
            this.ScriptConfig = new ProcessStartInfo();
            this.ScriptConfig.FileName = "run_core";
            this.ScriptConfig.Arguments = $"--core {this.Json} --port {this.Port}";
            this.ScriptConfig.WindowStyle = ProcessWindowStyle.Hidden;
            
            this.Client.Proxy = GlobalProxySelection.GetEmptyWebProxy();
            this.Client.BaseAddress = $"http://localhost:{this.Port}";
            this.Client.Headers = null;
        }

        public void Initialize()
        {
            ServerProcess = Process.Start(ScriptConfig);
            System.Threading.Thread.Sleep(5000);
        }

        public abstract TFuncType Calculate(Dictionary<string, TFuncType> values);

        public void Terminate()
        {
            ServerProcess.Kill();
        }
    }
}