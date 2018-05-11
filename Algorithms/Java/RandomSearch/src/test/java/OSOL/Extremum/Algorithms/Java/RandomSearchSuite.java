package OSOL.Extremum.Algorithms.Java;

import OSOL.Extremum.Cores.JVM.Optimization.Algorithm;
import OSOL.Extremum.Cores.JVM.Optimization.Testing.RealTester;
import OSOL.Extremum.Cores.JVM.Vectors.RealVector;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import scala.collection.JavaConverters;


public class RandomSearchSuite {

    double r = 1.0;
    double oneMin = 60.0;

    @Test
    void TestRandomSearch()
    {
        RealTester tester = new RealTester();
        List<Algorithm<RealVector, Double, RealVector>> configsToTest = new ArrayList<>();
        configsToTest.add(RandomSearch.createFixedStepRandomSearch(1.0 * r, 1 * oneMin));
        configsToTest.add(RandomSearch.createFixedStepRandomSearch(0.5 * r, 2 * oneMin));
        configsToTest.add(RandomSearch.createFixedStepRandomSearch(0.1 * r, 5 * oneMin));

        assertTrue(tester.apply(JavaConverters.iterableAsScalaIterable(configsToTest).toSeq()));
    }
}
