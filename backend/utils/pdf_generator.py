from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime
import io

class PDFReportGenerator:
    """Generate professional PDF reports for content analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#0284c7'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection style
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#475569'),
            spaceAfter=8,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        # Custom body text (not using existing BodyText)
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=6,
            alignment=TA_JUSTIFY
        ))
        
        # Recommendation style
        self.styles.add(ParagraphStyle(
            name='RecommendationText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#0369a1'),
            spaceAfter=6,
            leftIndent=20,
            bulletIndent=10
        ))
        
        # Issue style
        self.styles.add(ParagraphStyle(
            name='IssueText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#dc2626'),
            spaceAfter=6,
            leftIndent=20
        ))
        
        # Strength style
        self.styles.add(ParagraphStyle(
            name='StrengthText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#16a34a'),
            spaceAfter=6,
            leftIndent=20
        ))
    
    def generate_report(self, results, output_path=None):
        """
        Generate PDF report from analysis results
        
        Args:
            results: Dict containing analysis results
            output_path: Optional path to save PDF, if None returns BytesIO
            
        Returns:
            BytesIO object containing PDF data if output_path is None
        """
        # Create document
        if output_path:
            doc = SimpleDocTemplate(output_path, pagesize=letter,
                                   rightMargin=0.75*inch, leftMargin=0.75*inch,
                                   topMargin=1*inch, bottomMargin=0.75*inch)
        else:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                   rightMargin=0.75*inch, leftMargin=0.75*inch,
                                   topMargin=1*inch, bottomMargin=0.75*inch)
        
        # Build content
        story = []
        
        # Add header
        story.extend(self._create_header(results))
        
        # Add overall summary
        story.extend(self._create_overall_summary(results))
        
        # Add score visualization
        story.extend(self._create_score_chart(results))
        
        # Add detailed sections for each metric
        story.extend(self._create_seo_section(results.get('seo', {})))
        story.extend(self._create_serp_section(results.get('serp_performance', {})))
        story.extend(self._create_aeo_section(results.get('aeo', {})))
        story.extend(self._create_humanization_section(results.get('humanization', {})))
        story.extend(self._create_differentiation_section(results.get('differentiation', {})))
        
        # Add footer with generation date
        story.extend(self._create_footer())
        
        # Build PDF
        doc.build(story)
        
        if not output_path:
            buffer.seek(0)
            return buffer
    
    def _create_header(self, results):
        """Create report header"""
        elements = []
        
        # Title
        title = Paragraph("Content Quality Audit Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Metadata table
        metadata = [
            ['Analysis Date:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
            ['Word Count:', f"{results.get('word_count', 0):,} words"],
        ]
        
        if results.get('target_keyword'):
            metadata.append(['Target Keyword:', results['target_keyword']])
        
        if results.get('url'):
            metadata.append(['Source URL:', results['url']])
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4.5*inch])
        metadata_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#475569')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1e293b')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_overall_summary(self, results):
        """Create overall summary section"""
        elements = []
        
        overall_score = results.get('overall_score', 0)
        
        # Overall score display
        score_data = [[
            Paragraph('<b>Overall Content Quality Score</b>', self.styles['CustomBody']),
            Paragraph(f'<b><font size="24" color="#0284c7">{overall_score}/100</font></b>', self.styles['CustomBody'])
        ]]
        
        score_table = Table(score_data, colWidths=[4*inch, 2.5*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#0284c7')),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        elements.append(score_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Score interpretation
        if overall_score >= 80:
            interpretation = "Excellent - Your content demonstrates high quality across all dimensions."
        elif overall_score >= 60:
            interpretation = "Good - Your content is solid but has room for improvement in some areas."
        elif overall_score >= 40:
            interpretation = "Needs Improvement - Several areas require attention to enhance content quality."
        else:
            interpretation = "Poor - Significant improvements are needed across multiple dimensions."
        
        elements.append(Paragraph(interpretation, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_score_chart(self, results):
        """Create visual score breakdown"""
        elements = []
        
        elements.append(Paragraph("Score Breakdown", self.styles['SectionHeader']))
        
        # Scores table
        scores_data = [
            ['Metric', 'Score', 'Status'],
            ['SEO Score', f"{results.get('seo', {}).get('score', 0)}/100", self._get_status_text(results.get('seo', {}).get('score', 0))],
            ['SERP Performance', f"{results.get('serp_performance', {}).get('score', 0)}/100", self._get_status_text(results.get('serp_performance', {}).get('score', 0))],
            ['AEO Score', f"{results.get('aeo', {}).get('score', 0)}/100", self._get_status_text(results.get('aeo', {}).get('score', 0))],
            ['Humanization', f"{results.get('humanization', {}).get('score', 0)}/100", self._get_status_text(results.get('humanization', {}).get('score', 0))],
            ['Differentiation', f"{results.get('differentiation', {}).get('score', 0)}/100", self._get_status_text(results.get('differentiation', {}).get('score', 0))],
        ]
        
        scores_table = Table(scores_data, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
        scores_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284c7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(scores_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _get_status_text(self, score):
        """Get status text based on score"""
        if score >= 80:
            return "✓ Excellent"
        elif score >= 60:
            return "○ Good"
        elif score >= 40:
            return "△ Needs Work"
        else:
            return "✗ Poor"
    
    def _create_seo_section(self, seo_data):
        """Create SEO analysis section"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("SEO Score Analysis", self.styles['SectionHeader']))
        elements.append(Paragraph(f"Score: {seo_data.get('score', 0)}/100", self.styles['SubSection']))
        
        # Strengths
        good_points = seo_data.get('good_points', [])
        if good_points:
            elements.append(Paragraph("Strengths", self.styles['SubSection']))
            for point in good_points:
                elements.append(Paragraph(f"✓ {point}", self.styles['StrengthText']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Issues
        issues = seo_data.get('issues', [])
        if issues:
            elements.append(Paragraph("Issues Found", self.styles['SubSection']))
            for issue in issues:
                elements.append(Paragraph(f"✗ {issue}", self.styles['IssueText']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Recommendations
        recommendations = seo_data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("Top Recommendations", self.styles['SubSection']))
            for i, rec in enumerate(recommendations, 1):
                elements.append(Paragraph(f"{i}. {rec}", self.styles['RecommendationText']))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_serp_section(self, serp_data):
        """Create SERP Performance section"""
        elements = []
        
        elements.append(Paragraph("SERP Performance Analysis", self.styles['SectionHeader']))
        elements.append(Paragraph(f"Score: {serp_data.get('score', 0)}/100", self.styles['SubSection']))
        
        # SERP Analysis data
        serp_analysis = serp_data.get('serp_analysis')
        if serp_analysis:
            elements.append(Paragraph("Competitive Analysis", self.styles['SubSection']))
            
            comparison_data = [
                ['Metric', 'Your Content', 'SERP Average'],
                ['Word Count', f"{serp_analysis.get('your_word_count', 0):,}", f"{serp_analysis.get('avg_word_count', 0):,}"],
                ['Topics Covered', str(serp_analysis.get('your_topics', 0)), str(serp_analysis.get('avg_topics', 0))],
            ]
            
            comparison_table = Table(comparison_data, colWidths=[2*inch, 2*inch, 2*inch])
            comparison_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0f2fe')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            elements.append(comparison_table)
            elements.append(Spacer(1, 0.15*inch))
            
            # Predicted position
            predicted = serp_data.get('predicted_position', 'Unknown')
            elements.append(Paragraph(f"<b>Predicted Ranking:</b> {predicted}", self.styles['CustomBody']))
            elements.append(Spacer(1, 0.15*inch))
            
            # Backlink potential
            backlink = serp_data.get('backlink_potential')
            if backlink:
                elements.append(Paragraph(f"<b>Backlink Potential:</b> {backlink.get('level', 'N/A')} ({backlink.get('score', 0)}/100)", self.styles['CustomBody']))
                if backlink.get('linkable_assets'):
                    assets_text = ', '.join(backlink['linkable_assets'])
                    elements.append(Paragraph(f"Linkable Assets: {assets_text}", self.styles['CustomBody']))
                elements.append(Spacer(1, 0.15*inch))
        
        # Issues and Recommendations
        issues = serp_data.get('issues', [])
        if issues:
            elements.append(Paragraph("Issues Found", self.styles['SubSection']))
            for issue in issues:
                elements.append(Paragraph(f"✗ {issue}", self.styles['IssueText']))
            elements.append(Spacer(1, 0.1*inch))
        
        recommendations = serp_data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("Top Recommendations", self.styles['SubSection']))
            for i, rec in enumerate(recommendations, 1):
                elements.append(Paragraph(f"{i}. {rec}", self.styles['RecommendationText']))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_aeo_section(self, aeo_data):
        """Create AEO Score section"""
        elements = []
        
        elements.append(Paragraph("AEO (Answer Engine Optimization) Score", self.styles['SectionHeader']))
        elements.append(Paragraph(f"Score: {aeo_data.get('score', 0)}/100", self.styles['SubSection']))
        
        # Strengths
        good_points = aeo_data.get('good_points', [])
        if good_points:
            elements.append(Paragraph("Strengths", self.styles['SubSection']))
            for point in good_points:
                elements.append(Paragraph(f"✓ {point}", self.styles['StrengthText']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Issues
        issues = aeo_data.get('issues', [])
        if issues:
            elements.append(Paragraph("Issues Found", self.styles['SubSection']))
            for issue in issues:
                elements.append(Paragraph(f"✗ {issue}", self.styles['IssueText']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Recommendations
        recommendations = aeo_data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("Top Recommendations", self.styles['SubSection']))
            for i, rec in enumerate(recommendations, 1):
                elements.append(Paragraph(f"{i}. {rec}", self.styles['RecommendationText']))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_humanization_section(self, human_data):
        """Create Humanization Score section"""
        elements = []
        
        elements.append(Paragraph("Humanization Score", self.styles['SectionHeader']))
        elements.append(Paragraph(f"Score: {human_data.get('score', 0)}/100", self.styles['SubSection']))
        
        # Strengths
        good_points = human_data.get('good_points', [])
        if good_points:
            elements.append(Paragraph("Strengths", self.styles['SubSection']))
            for point in good_points:
                elements.append(Paragraph(f"✓ {point}", self.styles['StrengthText']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Issues
        issues = human_data.get('issues', [])
        if issues:
            elements.append(Paragraph("Issues Found", self.styles['SubSection']))
            for issue in issues:
                elements.append(Paragraph(f"✗ {issue}", self.styles['IssueText']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Recommendations
        recommendations = human_data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("Top Recommendations", self.styles['SubSection']))
            for i, rec in enumerate(recommendations, 1):
                elements.append(Paragraph(f"{i}. {rec}", self.styles['RecommendationText']))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_differentiation_section(self, diff_data):
        """Create Differentiation Score section"""
        elements = []
        
        elements.append(Paragraph("Differentiation Score", self.styles['SectionHeader']))
        elements.append(Paragraph(f"Score: {diff_data.get('score', 0)}/100", self.styles['SubSection']))
        
        # Uniqueness analysis
        overlap = diff_data.get('overlap_analysis')
        if overlap:
            elements.append(Paragraph("Uniqueness Analysis", self.styles['SubSection']))
            elements.append(Paragraph(f"Content Similarity with Competitors: {overlap.get('avg_similarity', 'N/A')}", self.styles['CustomBody']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Unique elements
        unique_elements = diff_data.get('unique_elements_found', [])
        if unique_elements:
            elements.append(Paragraph("Unique Elements Found", self.styles['SubSection']))
            for element in unique_elements:
                elements.append(Paragraph(f"✓ {element}", self.styles['StrengthText']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Issues
        issues = diff_data.get('issues', [])
        if issues:
            elements.append(Paragraph("Issues Found", self.styles['SubSection']))
            for issue in issues:
                elements.append(Paragraph(f"✗ {issue}", self.styles['IssueText']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Recommendations
        recommendations = diff_data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("Top Recommendations", self.styles['SubSection']))
            for i, rec in enumerate(recommendations, 1):
                elements.append(Paragraph(f"{i}. {rec}", self.styles['RecommendationText']))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_footer(self):
        """Create report footer"""
        elements = []
        
        elements.append(Spacer(1, 0.5*inch))
        footer_text = f"""
        <para align="center">
        <font size="8" color="#64748b">
        This report was generated by Content Quality Audit Tool on {datetime.now().strftime('%B %d, %Y')}<br/>
        © 2025 BEASTBOYZ PROJECT. All rights reserved.
        </font>
        </para>
        """
        elements.append(Paragraph(footer_text, self.styles['Normal']))
        
        return elements
