package kaimere.kernels

import kaimere.real.objects.RealVector
import org.scalatest.FunSuite

@kaimere.exclude_tags.MatlabTest
class MatlabSimulinkSuite extends FunSuite {

  implicit class RichDouble(val value: Double) {
    def ~(that: RichDouble, eps: Double = 1e-2): Boolean = math.abs(this.value - that.value) < eps
  }

  test("Orientation Test") {

    val MatlabLocation = sys.env("MatlabEngineLocation")
    Matlab.initialize(MatlabLocation)

    val modelLocation = getClass.getResource("/MatlabSimulinkKernelTest/SpacecraftOrientation.slx").getFile
    val jsonLocation = getClass.getResource("/MatlabSimulinkKernelTest/SpacecraftOrientation.json").getFile
    val model = Matlab.loadSimulinkModel(
      model = modelLocation,
      jsonConfig = jsonLocation)
    val result = model.apply(RealVector("a" -> 6 * math.Pi, "b" -> -12 * math.Pi))

    Matlab.unloadSimulinkModel(modelLocation)

    Matlab.terminate()
    
    assert(result ~ (12 * math.Pi * math.Pi))

  }

}
