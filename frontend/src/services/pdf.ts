import { jsPDF } from 'jspdf'

export const pdfService = {
  cleanMarkdown(text: string): string {
    return text
      .replace(/#{1,6}\s/g, '') // Headers
      .replace(/\*\*/g, '') // Bold
      .replace(/\*/g, '') // Italic/List
      .replace(/\[(.*?)\]\(.*?\)/g, '$1') // Links
      .replace(/`/g, '') // Code
      .replace(/>\s/g, '') // Blockquotes
  },

  generatePdf(title: string, content: string) {
    const doc = new jsPDF()
    const cleanContent = this.cleanMarkdown(content)
    
    // Title
    doc.setFontSize(20)
    doc.setFont('helvetica', 'bold')
    doc.text(title, 20, 20)
    
    // Content
    doc.setFontSize(12)
    doc.setFont('helvetica', 'normal')
    
    const splitText = doc.splitTextToSize(cleanContent, 170)
    
    let y = 40
    for (let i = 0; i < splitText.length; i++) {
      if (y > 280) {
        doc.addPage()
        y = 20
      }
      doc.text(splitText[i], 20, y)
      y += 7
    }
    
    doc.save(`${title.replace(/\s+/g, '_').toLowerCase()}.pdf`)
  }
}
