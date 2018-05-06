package OSOL.Extremum.Cores

import java.io.{File, PrintWriter}

/** Set of code tools */
package object JVM {

  /** Pipeline from Haskell */
  implicit class Pipe[I](val x: I) {
    def |>[O](f: I => O): O = f(x)
  }

  def deleteDirectory(file: File): Unit = {
    val contents = file.listFiles
    if (contents != null) for (f <- contents) {
      deleteDirectory(f)
    }
    file.delete
  }

  def extractResource(filename: String, suffix: String, location: String = "", where: String = "."): File  = {
    val libStream = getClass.getResourceAsStream(s"/$location/$filename.$suffix")
    val whereToPut = new File(where)
    if (!whereToPut.exists())  whereToPut.mkdirs()
    val tmpFile = new File(s"$whereToPut/$filename.$suffix")
    tmpFile.createNewFile()

    val buffer = scala.io.Source.fromInputStream(libStream)
    val writer = new PrintWriter(tmpFile)
    buffer.getLines().foreach(l => writer.println(l))
    writer.close()
    libStream.close()

    tmpFile
  }

}
