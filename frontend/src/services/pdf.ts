import { jsPDF } from 'jspdf'

export const pdfService = {
  generatePdf(title: string, content: string) {
    const doc = new jsPDF()
    const pageWidth = doc.internal.pageSize.getWidth()
    const pageHeight = doc.internal.pageSize.getHeight()
    const margin = 20
    const maxWidth = pageWidth - (margin * 2)
    
    // Heuristic to adjust font size based on content length
    // Goal: Fit in 1 page if possible, max 2 pages.
    let baseFontSize = 11
    let lineHeightFactor = 5 // Default spacing
    
    if (content.length > 4500) {
      baseFontSize = 9
      lineHeightFactor = 4
    } else if (content.length > 3000) {
      baseFontSize = 10
      lineHeightFactor = 4.5
    }

    let y = 20
    
    // Title
    doc.setFontSize(18)
    doc.setFont('helvetica', 'bold')
    doc.text(title, margin, y)
    y += 15
    
    // Process content line by line
    const lines = content.split('\n')
    
    doc.setFontSize(baseFontSize)
    
    for (let i = 0; i < lines.length; i++) {
      let line = lines[i].trim()
      
      // Check for page break
      if (y > pageHeight - margin) {
        doc.addPage()
        y = 20
      }
      
      if (!line) {
        y += lineHeightFactor
        continue
      }
      
      // Headers
      if (line.startsWith('#')) {
        const level = line.match(/^#+/)?.[0].length || 0
        const text = line.replace(/^#+\s*/, '')
        
        doc.setFont('helvetica', 'bold')
        // H1 = base+5, H2 = base+3, H3 = base+1
        const size = Math.max(baseFontSize + 1, baseFontSize + 6 - (level * 2))
        doc.setFontSize(size)
        
        y += lineHeightFactor
        
        // Check page break before header
        if (y > pageHeight - margin) {
            doc.addPage()
            y = 20
        }

        doc.text(text, margin, y)
        y += (size / 2) + 2
        
        // Reset to normal
        doc.setFont('helvetica', 'normal')
        doc.setFontSize(baseFontSize)
        continue
      }
      
      // List items
      let xOffset = margin
      if (line.startsWith('- ') || line.startsWith('* ')) {
        line = '• ' + line.substring(2)
        xOffset += 5
      }
      
      // Bold text cleanup
      const cleanLine = line.replace(/\*\*(.*?)\*\*/g, '$1').replace(/\*(.*?)\*/g, '$1')
      
      const splitText = doc.splitTextToSize(cleanLine, maxWidth - (xOffset - margin))
      
      for (const textLine of splitText) {
        if (y > pageHeight - margin) {
          doc.addPage()
          y = 20
        }
        doc.text(textLine, xOffset, y)
        y += lineHeightFactor
      }
    }
    
    doc.save(`${title.replace(/\s+/g, '_').toLowerCase()}.pdf`)
  }
}
