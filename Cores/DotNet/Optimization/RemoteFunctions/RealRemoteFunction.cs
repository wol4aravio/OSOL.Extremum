using System;
using System.Collections.Generic;
using System.Linq;

namespace OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions
{
    public class RealRemoteFunction: RemoteFunction<double>
    {
                
        public RealRemoteFunction(string json, int port, string field) : base(json, port, field)
        {
            
        }

        public sealed override double Calculate(Dictionary<string, double> values)
        {
            string url = $"process_request?field={this.Field}";
            url += values.Select(kvp => $"&{kvp.Key}={kvp.Value}").Aggregate("", (p1, p2) => p1 + p2);
            var request = Client.DownloadString(url);
            
            return Convert.ToDouble(request);
        }
    }
}