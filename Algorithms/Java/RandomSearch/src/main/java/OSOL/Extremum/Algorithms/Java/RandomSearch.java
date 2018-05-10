package OSOL.Extremum.Algorithms.Java;

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval;
import OSOL.Extremum.Cores.JVM.Optimization.*;
import OSOL.Extremum.Cores.JVM.Optimization.Nodes.*;
import OSOL.Extremum.Cores.JVM.Random.GoRN;
import OSOL.Extremum.Cores.JVM.Vectors.RealVector;
import OSOL.Extremum.Cores.JVM.Vectors.RealVector.Converters.*;

import scala.Tuple2;
import scala.collection.immutable.Map;
import scala.collection.JavaConverters;

import java.lang.*;
import java.util.*;

public class RandomSearch {

    private String currentPointName = "currentPoint";
    private String currentPointEfficiencyName = "currentPointEfficiency";
    private String radiusParameterName = "r";

    private RealVector generateRandomInSphere(RealVector currentPoint, Double radius, Map<String, Tuple2<Double, Double>> area)
    {
        RealVector normallyDistributed = GoRN.getNormal(area.mapValues(_ -> Tuple2.apply(0.0, 1.0)));
        int dim = currentPoint.elements().size();
        List<Double> values = JavaConverters.seqAsJavaList(normallyDistributed.elements().values().toSeq());

        double r = 0.0;
        for(Double v: values)
            r += v.doubleValue() * v;

        Double moveCoefficient = (GoRN.getContinuousUniform(-1.0, 1.0) / r);

        return (currentPoint.add(normallyDistributed.multiply(moveCoefficient))).constrain(area);
    }

}
