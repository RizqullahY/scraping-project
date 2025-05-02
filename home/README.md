# Comic Reader Project

## Background

I have a hobby of reading comics online on websites like [komikindo.id](https://komikindo.id), [webtoon](https://webtoon.com), [id.shinigami.ae](https://id.shinigami.ae), and others. However, I faced a problem:  
- When the internet was good, I was often busy and didn't have time to read.
- When I finally had free time, the internet would become very slow.

This situation was frustrating and disrupted my comic reading experience.

## Idea

I thought:  
*"What if I download the comic images from these platforms and read them offline?"*  
This way, I could download when the internet is stable and read whenever I want, even without a good connection.

## Research

After checking, I found that comic images from **komikindo.id** could be downloaded easily.  
That opened the way for me to implement my idea.

## Implementation

1. **Scraping Script**  
   I created a Python script to scrape and download the comic images automatically.

2. **Offline Comic Reader (HTML/CSS/JS)**  
   Even though I could view the images manually using the system's image previewer, it was uncomfortable for continuous reading.  
   So, I built a simple website (using just HTML, CSS, JS — and maybe some TailwindCSS and jQuery) to display the comics nicely.

   **Why not use React or other libraries?**  
   Because it's too much hassle for this simple purpose. Plain HTML/CSS/JS is enough for me.

3. **Responsive Image Size**  
   I added dynamic width control for the images, so I could adjust the image display according to my preference.

4. **Auto Scroll Feature**  
   I implemented auto-scroll functionality to make reading easier and more enjoyable, along with customizable scroll speed.

5. **Handling Image Tag Limitations**  
   Initially, I manually created 50 `<img>` tags in the HTML file.  
   However:
   - If there were more images than tags, some images wouldn't be displayed.
   - If there were fewer images, empty tags would show the `alt` text.

   To solve this, I made a **Python script** to automatically generate the correct number of `<img>` tags based on the downloaded images.

6. **Optimizing Performance**  
   I noticed that loading hundreds of images at once made the page heavy.  
   So, I implemented JavaScript logic to **load images one by one**, improving performance significantly.

## Performance Testing

- **117 images tested**

<div align="center">
  <table>
    <tr>
      <td align="center">
        <strong>index.html</strong><br>
        <img src="https://github.com/user-attachments/assets/c3254607-310c-4682-963a-6bbc4eed19be" width="200px">
      </td>
      <td align="center">
        <strong>index-V2.html</strong><br>
        <img src="https://github.com/user-attachments/assets/ac7ad466-3ed9-4b63-9dcf-3f6c09fea5bc" width="200px">
      </td>
    </tr>
  </table>
</div>

## Implementation 2
### Overview

Previously, whenever I wanted to read content, I had to manually copy files from the `temp` folder to the `image` folder. Even though I used shortcuts to ease this process, it still felt inconvenient and time-consuming.

To solve this, I created **version 2.1**, which automatically includes a pre-modified `index.html` file in every downloaded folder inside `/website/image-with-html/temp/`. This enhancement makes reading and navigating much easier and more efficient.

### Features

- Each download folder now includes an `index.html` file for immediate viewing.
- The Python script has been updated and placed in the same directory:  
  `/website/image-with-html-shorcut/`
- Shortcut links now directly point to:  
  `/website/image-with-html/`

With these updates, the workflow is smoother and more automated, significantly improving the user experience.

