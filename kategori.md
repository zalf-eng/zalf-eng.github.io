---
layout: page
title: Kategori
permalink: /kategori/
---

{% for category in site.categories %}
## {{ category[0] | replace: '-', ' ' | capitalize }}

{% for post in category[1] %}
- [{{ post.title }}]({{ post.url | relative_url }}) <small>({{ post.date | date: "%d-%m-%Y" }})</small>
{% endfor %}
{% endfor %}
