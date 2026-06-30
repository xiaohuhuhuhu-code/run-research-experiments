# Word Format Checklist

Use this checklist for Chinese DOCX/Word manuscript generation, revision, and final QA.

## Body Text

- Chinese body font: 宋体.
- English text, numbers, variables, model names, and identifiers: Times New Roman.
- Body font size: 小四.
- Font color: default black.
- Paragraph first-line indent: 2 Chinese characters.
- Alignment: justified.
- Line spacing: fixed 22 pt.
- Style: academic, concise, clear, not overly colloquial.
- Mixed Chinese/English/numeric terms should be visually coordinated.
- Use Chinese double quotation marks “ ” in Chinese prose, and fix final layout if a quotation mark appears as the first visible character of a line.

## Titles And Navigation

- Main title: 宋体 四号 bold, default black, centered, no first-line indent.
- First-level headings: 宋体 四号 bold, no first-line indent.
- Use Word built-in `Heading 1`, `Heading 2`, and `Heading 3` styles for first-, second-, and third-level headings.
- Confirm the Word left navigation pane shows an interactive outline.

## Tables

- Every table has an independent table title.
- Table title is above the table, centered, and 五号.
- Use three-line table style.
- Table content is vertically and horizontally centered.
- No first-line indent inside table cells.
- Table Chinese font: 宋体.
- Table English text, numbers, variables, and model names: Times New Roman.
- Table font size: 五号.
- Table line spacing: single.
- Keep decimal places consistent within each metric column.
- Avoid crowded pages by shortening field names or splitting large tables.
- Avoid table page breaks when possible. If a table must cross pages, use a continuation table.
- Do not compress table text shapes or enable “fit text”.
- Keep formula-like variables, subscripts, superscripts, and Greek letters as `$...$` LaTeX text under the DOCX formula policy.

## Table Explanation Paragraphs

- Every table is followed by one concise explanatory paragraph.
- Use body formatting: 宋体 小四, Times New Roman for English/numbers, first-line indent 2 characters, justified, fixed 22 pt.
- Explain the table role, field meanings, and position in the research content.
- Include one concrete example when useful, but keep it short for report-style presentation.

## Layout

- The document is optimized for clear report presentation.
- Keep table title, table, and table explanation together where feasible.
- Keep figure and caption together where feasible.
- Leave appropriate spacing between adjacent tables and avoid table stacking without explanation.
- If a table is long, split it, adjust row height/column width, or use continuation tables.

## Terminology And Concept Boundaries

- Keep important concept names consistent throughout the document.
- If applicable, preserve exact terms such as “学生个人私有知识库”, “课堂行为倾向”, “知识生成适应性引擎”, “多源异构特征对齐”, and “动态匹配机制”.
- Keep concept boundaries explicit. For example, the student personal/private knowledge base does not include classroom behavior; classroom behavior tendency is a separate behavior-side feature; they are fused only in the knowledge-generation adaptive engine stage.
- For other domains, write equivalent boundary notes for concepts that are easy to confuse.

## Final QA

- Export DOCX to PDF and visually inspect pages.
- Confirm body fixed 22 pt line spacing and 2-character first-line indent.
- Confirm Word heading styles drive the navigation pane outline.
- Confirm table titles are above tables and every table has a following explanation paragraph.
- Confirm three-line tables, table font size 五号, single line spacing, no table-cell first-line indent, and no crowded table pages.
- Confirm table text is not compressed and “fit text” is disabled.
- Confirm long tables are split or continued correctly.
- Confirm formulas remain visible as `$...$` LaTeX text and no DOCX OMML formula tags were generated.
- Confirm Chinese double quotation marks and line-start punctuation are acceptable after PDF export.
- Confirm terminology and conceptual boundaries are consistent.
- Report any remaining limitations.
