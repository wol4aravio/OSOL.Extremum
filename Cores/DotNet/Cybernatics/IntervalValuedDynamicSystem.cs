using System;
using OSOL.Extremum.Cores.DotNet.Arithmetics;
using OSOL.Extremum.Cores.DotNet.Vectors;

namespace OSOL.Extremum.Cores.DotNet.Cybernatics
{
    public class IntervalValuedDynamicSystem : DynamicSystem<Interval>
    {
        public IntervalValuedDynamicSystem(Func<VectorObject<Interval>, VectorObject<Interval>> f, Func<VectorObject<Interval>, VectorObject<Interval>> u, ButcherTableau butcherTableau)
        {
            this.f = f;
            this.u = u;
            this.butcherTableau = butcherTableau;
        }

        public sealed override double BaseToDouble(Interval b) => b.MiddlePoint;

        public sealed override Interval DoubleToBase(double d) => d;
    }
}