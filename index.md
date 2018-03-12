<ul>
  {% for post in site.posts reversed %}
    {% unless post.draft %}
      <li>
        <a href="{{ site.baseurl }}{{ post.url }}">{{ post.date | date: "%Y-%m-%d"}} {{ post.title }}</a>
      </li>
    {% endunless %}
  {% endfor %}
</ul>
