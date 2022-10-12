import java.io.File;
import java.io.FileReader;
import java.io.Reader;
import java.io.StringReader;
import java.io.FileNotFoundException;
import java.nio.file.Paths;
import java.util.Iterator;
import java.util.regex.Pattern;

import cc.mallet.grmm.learning.ACRF;
import cc.mallet.util.FileUtils;
import cc.mallet.pipe.Pipe;
import cc.mallet.types.Instance;
import cc.mallet.types.InstanceList;
import cc.mallet.types.FeatureVectorSequence;
import cc.mallet.types.LabelsSequence;
import cc.mallet.pipe.iterator.LineGroupIterator;

public class AcrfPredict {

  public static String parseVectorLabel(FeatureVectorSequence vectors, LabelsSequence labels) {
    String result = "";
    String vectorString = "";
    String word = "";
    String label = "";

    for (int i = 0; i < vectors.size(); i++) {
      vectorString = vectors.get(i).toString();
      label = labels.getLabels(i).get(0).toString();
      word = vectorString.substring(vectorString.lastIndexOf("\n", vectorString.indexOf("@0")) + 1,
          vectorString.indexOf("@0"));

      switch (label) {
        case "PERIOD":
          word += ". ";
          break;
        case "COMMA":
          word += ", ";
          break;
        case "QMARK":
          word += "? ";
          break;
        default:
          word += " ";
          break;
      }

      result += word;
    }

    return result.trim();
  }

  public static void main(String[] args) throws FileNotFoundException {
    String filepath = args[0];
    File inputFile = new File(filepath);
    Reader reader = new FileReader(inputFile);
    ACRF c = (ACRF) FileUtils.readObject(Paths.get("acrf.ser.gz").toFile());

    Pipe pipe = c.getInputPipe();
    InstanceList testing = new InstanceList(pipe);
    LineGroupIterator testSource = new LineGroupIterator(
        reader, Pattern.compile("^\\s*$"), true);

    testing.addThruPipe(testSource);

    for (int i = 0; i < testing.size(); i++) {
      FeatureVectorSequence vectors = (FeatureVectorSequence) testing.get(i).getData();
      LabelsSequence labels = c.getBestLabels(testing.get(i));
      System.out.println(parseVectorLabel(vectors, labels));
    }
  }
}