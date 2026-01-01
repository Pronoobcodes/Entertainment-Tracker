<div class="col-6 col-sm-4 col-md-3 col-lg-2">
    <div class="movie-card position-relative">

        {% if item.poster %}
            <img src="{{ item.poster }}" class="w-100 poster">
        {% else %}
            <div class="poster bg-secondary"></div>
        {% endif %}

        <span class="badge bg-danger badge-source">
            {{ item.source|upper }}
        </span>

        <div class="movie-info">
            <div class="movie-title">{{ item.title }}</div>
            <div class="movie-meta">
                {{ item.media_type|title }}
                {% if item.release_year %}
                    • {{ item.release_year }}
                {% endif %}
            </div>
        </div>
    </div>
</div>
