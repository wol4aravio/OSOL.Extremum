using System;

namespace OSOL.Extremum.Core.DotNet.Vectors
{
    public static class VectorExceptions
    {
        public class MissingKeyException : Exception
        {
            private readonly string _missingKey;

            public MissingKeyException(string missingKey)
            {
                this._missingKey = string.Copy(missingKey);
            }

            public override string Message => $"{_missingKey} is not present in current VectorObject";
        }

        public class DifferentKeysException : Exception
        {
            private readonly string[] _keys_1, _keys_2;

            public DifferentKeysException(string[] keys_1, string[] keys_2)
            {
                this._keys_1 = new string[keys_1.Length];
                this._keys_2 = new string[keys_2.Length];
                
                Array.Copy(keys_1, _keys_1, keys_1.Length);
                Array.Copy(keys_2, _keys_2, keys_2.Length);
            }

            public override string Message => $"VectorObjects have different set of keys: {_keys_1} and {_keys_2}";
        }
    }
}