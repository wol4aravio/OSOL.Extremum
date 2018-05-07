using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json.Linq;

using OSOL.Extremum.Cores.DotNet.Arithmetics;

namespace OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions
{
    public class IntervalRemoteFunction: RemoteFunction<Interval>
    {

        public IntervalRemoteFunction(string json, int port, string field) : base(json, port, field)
        {
            
        }

        public sealed override Interval Calculate(Dictionary<string, Interval> values)
        {
            string url = $"http://localhost:{this.Port}/process_request?field={this.Field}&scope=interval";
            url += values.Select(kvp => $"&{kvp.Key}={kvp.Value.ConvertToJson().ToString()}").Aggregate("", (p1, p2) => p1 + p2);
            var request = JObject.Parse(Client.DownloadString(url));

            return new Interval(request);
        }
    }

}