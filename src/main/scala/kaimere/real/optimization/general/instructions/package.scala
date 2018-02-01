package kaimere.real.optimization.general

import java.text.DecimalFormat

package object instructions {

  def truncate(d: Double): String = new DecimalFormat("#.##").format(d)

}
