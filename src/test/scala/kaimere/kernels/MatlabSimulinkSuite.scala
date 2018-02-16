package kaimere.kernels

import kaimere.real.objects.RealVector

import org.scalatest.{BeforeAndAfterAll, FunSuite}

class MatlabSimulinkSuite extends FunSuite with BeforeAndAfterAll {

  implicit class RichDouble(val value: Double) {
    def ~(that: RichDouble, eps: Double = 1e-3): Boolean = math.abs(this.value - that.value) < eps
  }

  override def beforeAll(): Unit = {
    val MatlabLocation = sys.env("MatlabEngineLocation")
    Matlab.initialize(MatlabLocation)
  }

  test("Orientation Test") {
    val modelLocation = getClass.getResource("/MatlabSimulinkKernelTest/SpacecraftOrientation.slx").getFile
    val jsonLocation = getClass.getResource("/MatlabSimulinkKernelTest/SpacecraftOrientation.json").getFile
    val model = Matlab.loadSimulinkModel(
      model = modelLocation,
      jsonConfig = jsonLocation)
    val result = model.apply(RealVector("a" -> 6 * math.Pi, "b" -> -12 * math.Pi))

    Matlab.unloadSimulinkModel(modelLocation)

    assert(result ~ (12 * math.Pi * math.Pi))
  }

  override def afterAll(): Unit = {
    Matlab.terminate()
  }

}
