---
layout: blog
title: Blog
permalink: /blog/
---
<div class="content">
  <h1>Blog</h1>
  <ul class="post-list">
    {% for post in site.posts %}
    <li class="post-item">
      <span class="post-date">{{ post.date | date: "%d/%m/%y" }}</span>
      <a href="{{ post.url | relative_url }}" class="post-title">{{ post.title }}</a>
    </li>
    {% endfor %}
  </ul>
</div>
