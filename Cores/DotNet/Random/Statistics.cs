using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;

namespace OSOL.Extremum.Cores.DotNet.Random
{
    public static class Statistics
    {

        public static double SampleMoment(IEnumerable<double> data, int n) =>
            data.Select(x => Math.Pow(x, n)).Average();

        public static double GetMean(IEnumerable<double> data) => SampleMoment(data, n: 1);

        public static double CentralMoment(IEnumerable<double> data, int n)
        {
            double[] dataArray = data as double[] ?? data.ToArray();
            double average = GetMean(dataArray);
            return dataArray.Select(x => Math.Pow(x - average, n)).Average();
        }

        public static double GetUnbiasedSigma(IEnumerable<double> data)
        {
            double[] dataArray = data as double[] ?? data.ToArray();
            double size = dataArray.Count();
            return Math.Sqrt(CentralMoment(dataArray, 2) * (size / (size - 1)));
        }

    }
}