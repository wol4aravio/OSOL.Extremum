using System;

namespace OSOL.Extremum.Cores.DotNet.Arithmetics
{
    public static class IntervalExceptions
    {
        public class MinMaxFailureException : Exception
        {
            private readonly double _min, _max;

            public MinMaxFailureException(double min, double max)
            {
                this._min = min;
                this._max = max;
            }
        }
        
        public class UnknownOperationException : Exception
        {
            private readonly string _opName;

            public UnknownOperationException(string opName)
            {
                this._opName = opName;
            }
        }
        
        public class BadAreaOperationException : Exception
        {
            private readonly string _opName;
            private readonly Interval _interval;

            public BadAreaOperationException(string opName, Interval interval)
            {
                this._opName = opName;
                this._interval = interval;
            }
        }

    }
}