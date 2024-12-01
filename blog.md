---
layout: default
title: Blog
---
<div class="content">
  <h1>Blog</h1>
  <ul>
    {% for post in site.posts %}
    <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
</div>