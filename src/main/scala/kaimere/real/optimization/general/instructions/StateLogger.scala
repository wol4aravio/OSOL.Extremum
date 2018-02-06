package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import java.io._

import spray.json._

case class StateLogger(folderName: String, mainInstruction: GeneralInstruction) extends GeneralInstruction {

  private var iterationId = 1

  override def continue(algorithm: OptimizationAlgorithm): Boolean = {
    StateLogger.saveJson(algorithm.currentState.toJson, folderName, iterationId)
    iterationId += 1
    mainInstruction.continue(algorithm)
  }

  override def reset(): Unit = {
    iterationId = 1
    val folder = new File(folderName)
    if (folder.exists()) StateLogger.deleteFolder(folder)
    else folder.mkdirs()
  }

}

object StateLogger {

  def apply(csv: String): StateLogger = {
    val name = csv.split(",").head
    val folderName = csv.split(",").tail.head
    val instruction = csv.split(",").tail.tail
    name match {
      case "StateLogger" => StateLogger(folderName, GeneralInstruction.fromCsv(instruction.mkString(",")))
      case _ => throw DeserializationException("StateLogger expected")
    }
  }

  def deleteFolder(folder: File): Unit = {
    if (folder.isDirectory) folder.listFiles().foreach(deleteFolder)
    folder.delete
  }

  def saveJson(json: JsValue, folderName: String, id: Int): Unit = {
    val out = new BufferedWriter(new FileWriter(s"$folderName/$id.json"))
    out.write(json.prettyPrint)
    out.close()
  }

  implicit object StateLoggerJsonFormat extends RootJsonFormat[StateLogger] {
    def write(i: StateLogger) =
      JsObject(
        "name" -> JsString("StateLogger"),
        "folder" -> JsString(i.folderName),
        "mainInstruction" -> GeneralInstruction.toJson(i.mainInstruction))

    def read(json: JsValue): StateLogger =
      json.asJsObject.getFields("name", "folder", "mainInstruction") match {
        case Seq(JsString(name), JsString(folder), mainInstruction) =>
          if (name != "StateLogger") throw DeserializationException("StateLogger expected")
          else StateLogger(folder, GeneralInstruction.fromJson(mainInstruction))
        case _ => throw DeserializationException("StateLogger expected")
      }
  }

}