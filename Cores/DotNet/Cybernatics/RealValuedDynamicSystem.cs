using System;
using OSOL.Extremum.Cores.DotNet.Vectors;

namespace OSOL.Extremum.Cores.DotNet.Cybernatics
{
    public class RealValuedDynamicSystem: DynamicSystem<double>
    {
        public RealValuedDynamicSystem(Func<VectorObject<double>, VectorObject<double>> f, Func<VectorObject<double>, VectorObject<double>> u, ButcherTableau butcherTableau)
        {
            this.f = f;
            this.u = u;
            this.butcherTableau = butcherTableau;
        }
        
        public sealed override double BaseToDouble(double b) => b;

        public sealed override double DoubleToBase(double d) => d;
    }
}