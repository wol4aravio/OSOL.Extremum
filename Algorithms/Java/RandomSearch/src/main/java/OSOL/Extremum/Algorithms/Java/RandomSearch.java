package OSOL.Extremum.Algorithms.Java;

import OSOL.Extremum.Cores.JVM.Optimization.*;
import OSOL.Extremum.Cores.JVM.Optimization.Nodes.*;
import OSOL.Extremum.Cores.JVM.Random.GoRN;
import OSOL.Extremum.Cores.JVM.Vectors.RealVector;

import scala.Function1;
import scala.Option;
import scala.Tuple2;
import scala.Tuple3;
import scala.collection.immutable.Map;
import scala.collection.JavaConverters;
import scala.collection.immutable.Map$;

import java.lang.*;
import java.util.*;

public class RandomSearch {

    private static String currentPointName = "currentPoint";
    private static String currentPointEfficiencyName = "currentPointEfficiency";
    private static String radiusParameterName = "r";

    private static RealVector generateRandomInSphere(RealVector currentPoint, Double radius, Map<String, Tuple2<Double, Double>> area) {
        RealVector normallyDistributed = RealVector.Converters.IterableToRealVector(GoRN.getNormal(area.mapValues(a -> Tuple2.apply(0.0, 1.0))));
        int dim = currentPoint.elements().size();
        List<Double> values = JavaConverters.seqAsJavaList(normallyDistributed.elements().values().toSeq());

        double r = 0.0;
        for (Double v : values)
            r += v.doubleValue() * v;

        Double moveCoefficient = (GoRN.getContinuousUniform(-1.0, 1.0) / r);

        return (currentPoint.add(normallyDistributed.multiply(moveCoefficient))).constrain(area);
    }

    public static final class GenerateInitialPointNode extends GeneralNode<RealVector, Double, RealVector> {
        @Override
        public void initialize(Function1<Map<String, Double>, Double> f, Map<String, Tuple2<Double, Double>> area, State<RealVector, Double, RealVector> state) {
            RealVector initialPoint = RealVector.Converters.IterableToRealVector(GoRN.getContinuousUniform(area));
            state.setParameter(currentPointName, initialPoint);
            state.setParameter(currentPointEfficiencyName, initialPoint.getPerformance(f));
        }

        @Override
        public void process(Function1<Map<String, Double>, Double> f, Map<String, Tuple2<Double, Double>> area, State<RealVector, Double, RealVector> state) {

        }

        public GenerateInitialPointNode(Integer nodeId) {
            super(nodeId);
        }
    }

    public static final class SampleNewPointNode_FixedStep extends GeneralNode<RealVector, Double, RealVector> {
        @Override
        public void initialize(Function1<Map<String, Double>, Double> f, Map<String, Tuple2<Double, Double>> area, State<RealVector, Double, RealVector> state) {

        }

        @Override
        public void process(Function1<Map<String, Double>, Double> f, Map<String, Tuple2<Double, Double>> area, State<RealVector, Double, RealVector> state) {
            RealVector currentPoint = state.getParameter(currentPointName);
            Double currentPointEfficiency = state.getParameter(currentPointEfficiencyName);
            Double r = state.getParameter(radiusParameterName);

            RealVector newPoint = generateRandomInSphere(currentPoint, r, area);
            Double newPointEfficiency = newPoint.getPerformance(f);

            if (newPointEfficiency < currentPointEfficiency) {
                state.setParameter(currentPointName, newPoint);
                state.setParameter(currentPointEfficiencyName, newPointEfficiency);
            }
        }

        public SampleNewPointNode_FixedStep(Integer nodeId) {
            super(nodeId);
        }
    }

    public static final class SetBestNode extends GeneralNode<RealVector, Double, RealVector> {
        @Override
        public void initialize(Function1<Map<String, Double>, Double> f, Map<String, Tuple2<Double, Double>> area, State<RealVector, Double, RealVector> state) {

        }

        @Override
        public void process(Function1<Map<String, Double>, Double> f, Map<String, Tuple2<Double, Double>> area, State<RealVector, Double, RealVector> state) {
            RealVector currentPoint = state.getParameter(currentPointName);
            state.result_$eq(Option.apply(currentPoint));
        }

        public SetBestNode(Integer nodeId) {
            super(nodeId);
        }
    }

    public static Algorithm<RealVector, Double, RealVector> createFixedStepRandomSearch(Double radius, Double maxTime) {
        Map<String, Object> parameters = Map$.MODULE$.<String, Object>empty().$plus(Tuple2.apply(radiusParameterName, radius));

        List<GeneralNode<RealVector, Double, RealVector>> FixedStep_nodes = new ArrayList<>();
        FixedStep_nodes.add(new SetParametersNode<>(0, parameters));
        FixedStep_nodes.add(new GenerateInitialPointNode(1));
        FixedStep_nodes.add(new TerminationViaMaxTime<>(2, maxTime, "startTime"));
        FixedStep_nodes.add(new SampleNewPointNode_FixedStep(3));
        FixedStep_nodes.add(new SetBestNode(4));

        List<Tuple3<Integer, Option<Integer>, Integer>> FixedStep_transitionMatrix = new ArrayList<>();
        FixedStep_transitionMatrix.add(Tuple3.apply(0, Option.empty(), 1));
        FixedStep_transitionMatrix.add(Tuple3.apply(1, Option.empty(), 2));
        FixedStep_transitionMatrix.add(Tuple3.apply(2, Option.apply(0), 3));
        FixedStep_transitionMatrix.add(Tuple3.apply(2, Option.apply(1), 4));
        FixedStep_transitionMatrix.add(Tuple3.apply(3, Option.empty(), 2));

        return new Algorithm<>(
                JavaConverters.iterableAsScalaIterable(FixedStep_nodes).toSeq(),
                JavaConverters.iterableAsScalaIterable(FixedStep_transitionMatrix).toSeq());
    }
}