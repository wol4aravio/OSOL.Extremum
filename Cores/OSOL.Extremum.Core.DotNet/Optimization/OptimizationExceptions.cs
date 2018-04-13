using System;
using System.Collections.Generic;

namespace OSOL.Extremum.Core.DotNet.Optimization
{
    
    public static class OptimizationExceptions
    {

        public class ParameterAlreadyExistsException : Exception
        {
            private readonly string _parameterName;

            public ParameterAlreadyExistsException(string parameterName)
            {
                this._parameterName = parameterName;
            }
        }

        public class NoSuchParameterException : Exception
        {
            private readonly string _parameterName;

            public NoSuchParameterException(string parameterName)
            {
                this._parameterName = parameterName;
            }
        }
    }
}