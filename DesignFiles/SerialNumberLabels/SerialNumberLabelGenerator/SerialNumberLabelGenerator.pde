
import processing.pdf.*;

/*
SERIAL NUMBER LABEL GENERATOR
Jeff Thompson | 2015 | www.jeffreythompson.org

*/

int serial =      0;
int padding =     8;
int numPages =    12;
float[] xCoords = { 230.464, 455.464 };
float[] yCoords = { 67, 148, 229, 310, 391, 472, 553, 639, 715 };

PGraphics pdf;
PGraphicsPDF pdfOutput;


void setup() {
  size(int(8.5*72), int(11*72));
  
  println("Opening PDF renderer...");
  pdf = createGraphics(width, height, PDF, "../SerialNumberLabels.pdf");
  pdfOutput = (PGraphicsPDF) pdf;
  pdf.beginDraw();
  
  println("Creating font...");
  PFont font = createFont("Century Gothic", 10);
  pdf.textFont(font, 10);
  pdf.textAlign(RIGHT);
  
  pdf.fill(0);
  pdf.noStroke();
  println("Generating PDFs...");
  for (int page=0; page<numPages; page++) {
    println("- " + (page+1) + "/" + numPages);
    for (int x=0; x<xCoords.length; x++) {
      for (int y=0; y<yCoords.length; y++) {
        pdf.text(nf(serial, padding), xCoords[x], yCoords[y]);
        serial += 1;
      }
    }
    
    if (page < numPages-1) {
      pdfOutput = (PGraphicsPDF) pdf;
      pdfOutput.nextPage();
    }
  }
  
  println("\nDONE!");
  pdf.dispose();
  pdf.endDraw();
  exit();
}


