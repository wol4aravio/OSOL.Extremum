package OSOL.Extremum.Algorithms.Java;

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval;
import OSOL.Extremum.Cores.JVM.Optimization.*;
import OSOL.Extremum.Cores.JVM.Optimization.Nodes.*;
import OSOL.Extremum.Cores.JVM.Random.GoRN;
import OSOL.Extremum.Cores.JVM.Vectors.RealVector;
import OSOL.Extremum.Cores.JVM.Vectors.RealVector.Converters.*;

import scala.Tuple2;
import scala.collection.immutable.Map;
import java.lang.*;

public class RandomSearch {

    private String currentPointName = "currentPoint";
    private String currentPointEfficiencyName = "currentPointEfficiency";
    private String radiusParameterName = "r";

    private RealVector generateRandomInSphere(RealVector currentPoint, Double radius, Map<String, Tuple2<Double, Double>> area)
    {
        RealVector normallyDistributed = GoRN.getNormal(area.mapValues(_ -> Tuple2.apply(0.0, 1.0)));
        Double r = normallyDistributed.elements().values().map(v -> v.doubleValue() * v);
    }

//    private def generateRandomInSphere(currentPoint: RealVector, radius: Double, area: Area): RealVector = {
//        val normallyDistributed = GoRN.getNormal(area.mapValues(_ => (0.0, 1.0)))
//        val r = math.sqrt(normallyDistributed.values.map(v => v * v).sum)
//        (currentPoint + normallyDistributed * (GoRN.getContinuousUniform(-1.0, 1.0) / r)).constrain(area)
//    }

}
