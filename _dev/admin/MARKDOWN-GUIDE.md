# Markdown Support in Admin Interfaces

Both the **Create** and **Edit** admin interfaces now support Markdown syntax in the **Description** and **Acknowledgment** fields!

## Supported Syntax

### Links
```markdown
[YouTube Video](https://www.youtube.com/watch?v=ni70-yjjfUE&t=5s)
[Official Website](https://www.example.com)
```

**Result:**  
[YouTube Video](https://www.youtube.com/watch?v=ni70-yjjfUE&t=5s)  
[Official Website](https://www.example.com)

---

### Text Formatting
```markdown
**Bold text**
*Italic text*
***Bold and italic***
```

**Result:**  
**Bold text**  
*Italic text*  
***Bold and italic***

---

### Lists

**Unordered:**
```markdown
- First item
- Second item
- Third item
```

**Result:**
- First item
- Second item
- Third item

**Ordered:**
```markdown
1. First step
2. Second step
3. Third step
```

**Result:**
1. First step
2. Second step
3. Third step

---

### Paragraphs

Just use blank lines to separate paragraphs:

```markdown
This is the first paragraph.

This is the second paragraph.
```

---

### Inline Code
```markdown
Use the `code()` function to process data.
```

**Result:**  
Use the `code()` function to process data.

---

### Headings (use sparingly)
```markdown
## Subheading
### Smaller heading
```

---

## Practical Examples

### Example 1: YouTube Link in Description

```markdown
This interactive installation was commissioned for the Montreal Museum.

Watch the [installation video on YouTube](https://www.youtube.com/watch?v=ni70-yjjfUE&t=5s) to see it in action.

The piece explores themes of memory and digital presence.
```

### Example 2: Multiple Links

```markdown
The project was featured in several publications:
- [The Guardian review](https://www.theguardian.com/article)
- [ArtForum feature](https://www.artforum.com/article)
- [Artist's statement](https://www.artist-site.com/statement)

Visit the [official project site](https://www.project.com) for more information.
```

### Example 3: Formatted Text

```markdown
The installation consists of **1,128 loudspeakers**, each playing a different composition. 

The piece is designed to create a *polyvocal and complex sound environment* that visitors can explore.

Key features:
- Multi-channel sound system
- Interactive response to visitor presence
- Custom-built electronics
```

### Example 4: Acknowledgment with Links

```markdown
Special thanks to the team at [Studio X](https://studiox.com) for their technical support.

Commissioned by the **Montreal Museum of Fine Arts** in collaboration with [Digital Arts Foundation](https://digitalarts.org).
```

---

## Tips

1. **Preview in Browser:** The live preview in the admin interface shows plain text, but the final page will render all Markdown formatting.

2. **External Links:** All links automatically open in a new tab (`target="_blank"`).

3. **Keep it Simple:** While many Markdown features are supported, stick to links, bold, italic, and lists for best results.

4. **Line Breaks:** Use blank lines between paragraphs for proper spacing.

5. **URLs in Text:** Don't paste raw URLs - always wrap them in Markdown link syntax for a cleaner look.

6. **Round-Trip Editing:** When you edit an existing project, the HTML is automatically converted back to Markdown in the form fields, so you can edit the Markdown syntax directly!

---

## Examples to Try

### Simple Project Description

```markdown
A large-scale interactive installation exploring human presence through light and sound.

The work responds to visitors' movements, creating unique patterns that reflect the collective behavior of the audience. Each interaction adds to an evolving visual and sonic landscape.

**Key Features:**
- Real-time motion tracking
- Generative visual algorithms
- Multi-channel audio system

Learn more on the [project website](https://www.example.com/project).
```

### With Multiple Links

```markdown
This project was developed over 18 months in collaboration with researchers at [MIT Media Lab](https://www.media.mit.edu/).

The installation premiered at [Ars Electronica](https://ars.electronica.art/) in Linz, Austria, and subsequently traveled to [ZKM](https://zkm.de/) in Karlsruhe, Germany.

Documentation: [Full photo gallery](https://photos.example.com) | [Video documentation](https://vimeo.com/12345)
```

---

## Compatibility

- ✅ Works in both Create and Edit interfaces
- ✅ Renders in final HTML pages
- ✅ Supports all standard Markdown syntax
- ✅ Preserves line breaks (`nl2br` extension)
- ✅ Supports tables, definition lists (via `extra` extension)
- ✅ **Round-trip conversion:** HTML automatically converts back to Markdown when editing existing projects!

---

## Need Help?

Just type Markdown syntax as you would in any Markdown editor. The formatting will automatically apply when you save the project!

