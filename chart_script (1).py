import plotly.graph_objects as go
import plotly.express as px

# Create a database schema diagram using Plotly
fig = go.Figure()

# Define table positions
tables = {
    'incidents': {'x': 0.2, 'y': 0.7, 'width': 0.25, 'height': 0.55},
    'grid_aggregates': {'x': 0.55, 'y': 0.4, 'width': 0.2, 'height': 0.25},
    'predictions': {'x': 0.55, 'y': 0.05, 'width': 0.2, 'height': 0.25}
}

# Define columns for each table
columns = {
    'incidents': [
        'incident_id (BIGINT) PK',
        'iucr (VARCHAR)',
        'primary_type (VARCHAR) IDX',
        'description (TEXT)',
        'district (INT) IDX',
        'community_area (INT)',
        'beat (INT)',
        'grid_id (VARCHAR) IDX FK',
        'geohash6 (VARCHAR) IDX',
        'geohash8 (VARCHAR)',
        'latitude (DOUBLE)',
        'longitude (DOUBLE)',
        'event_ts (DATETIME) IDX',
        'event_date (DATE) IDX',
        'event_hour (TINYINT)',
        'day_of_week (TINYINT)',
        'is_weekend (TINYINT)',
        'arrest (BOOLEAN)',
        'domestic (BOOLEAN)',
        'reported_year (SMALLINT)',
        'created_at (TIMESTAMP)',
        'updated_at (TIMESTAMP)'
    ],
    'grid_aggregates': [
        'grid_id (VARCHAR) PK',
        'date (DATE) PK',
        'hour (TINYINT) PK',
        'count (INT)',
        'rolling_1d (INT)',
        'rolling_7d (INT)',
        'rolling_30d (INT)'
    ],
    'predictions': [
        'id (INT) PK AUTO_INC',
        'grid_id (VARCHAR) IDX FK',
        'prediction_date (DATE) IDX',
        'prediction_hour (TINYINT)',
        'predicted_count (FLOAT)',
        'confidence (FLOAT)',
        'model_version (VARCHAR)',
        'created_at (TIMESTAMP)'
    ]
}

# Color scheme
colors = {
    'header': '#13343B',  # Dark blue
    'pk': '#D2BA4C',      # Yellow
    'idx': '#B3E5EC',     # Light blue  
    'fk': '#DB4545',      # Red
    'normal': '#F3F3EE',  # Light background
    'border': '#2E8B57'   # Green border
}

# Draw table rectangles and headers
for table_name, pos in tables.items():
    # Table border
    fig.add_shape(
        type="rect",
        x0=pos['x'], y0=pos['y'],
        x1=pos['x'] + pos['width'], y1=pos['y'] + pos['height'],
        line=dict(color=colors['border'], width=2),
        fillcolor=colors['normal']
    )
    
    # Header rectangle
    header_height = 0.04
    fig.add_shape(
        type="rect",
        x0=pos['x'], y0=pos['y'] + pos['height'] - header_height,
        x1=pos['x'] + pos['width'], y1=pos['y'] + pos['height'],
        line=dict(color=colors['border'], width=2),
        fillcolor=colors['header']
    )
    
    # Table name
    fig.add_annotation(
        x=pos['x'] + pos['width']/2,
        y=pos['y'] + pos['height'] - header_height/2,
        text=f"<b>{table_name}</b>",
        showarrow=False,
        font=dict(color='white', size=12),
        xanchor='center',
        yanchor='middle'
    )
    
    # Add columns
    col_height = (pos['height'] - header_height) / len(columns[table_name])
    for i, col in enumerate(columns[table_name]):
        y_pos = pos['y'] + pos['height'] - header_height - (i + 0.5) * col_height
        
        # Determine color based on column type
        text_color = 'black'
        bg_color = colors['normal']
        
        if 'PK' in col:
            text_color = colors['header']
            # Add yellow highlight for PK
            fig.add_shape(
                type="rect",
                x0=pos['x'] + 0.01, y0=y_pos - col_height/3,
                x1=pos['x'] + pos['width'] - 0.01, y1=y_pos + col_height/3,
                line=dict(color=colors['pk'], width=1),
                fillcolor=colors['pk'],
                opacity=0.3
            )
        elif 'FK' in col:
            text_color = colors['fk']
        elif 'IDX' in col:
            text_color = colors['header']
            # Add light blue highlight for IDX
            fig.add_shape(
                type="rect",
                x0=pos['x'] + 0.01, y0=y_pos - col_height/3,
                x1=pos['x'] + pos['width'] - 0.01, y1=y_pos + col_height/3,
                line=dict(color=colors['idx'], width=1),
                fillcolor=colors['idx'],
                opacity=0.3
            )
        
        fig.add_annotation(
            x=pos['x'] + 0.02,
            y=y_pos,
            text=col,
            showarrow=False,
            font=dict(color=text_color, size=8),
            xanchor='left',
            yanchor='middle'
        )

# Add relationship arrows
# incidents -> grid_aggregates
fig.add_annotation(
    x=0.45, y=0.6,
    ax=0.45, ay=0.65,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor=colors['border']
)

# grid_aggregates -> predictions  
fig.add_annotation(
    x=0.65, y=0.35,
    ax=0.65, ay=0.4,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor=colors['border']
)

# Add relationship labels
fig.add_annotation(
    x=0.47, y=0.62,
    text="1:M",
    showarrow=False,
    font=dict(color=colors['border'], size=10),
    xanchor='left'
)

fig.add_annotation(
    x=0.67, y=0.37,
    text="1:M", 
    showarrow=False,
    font=dict(color=colors['border'], size=10),
    xanchor='left'
)

# Add legend
legend_items = [
    ("PK = Primary Key", colors['pk']),
    ("IDX = Indexed", colors['idx']),
    ("FK = Foreign Key", colors['fk'])
]

for i, (text, color) in enumerate(legend_items):
    fig.add_annotation(
        x=0.05, y=0.25 - i*0.05,
        text=text,
        showarrow=False,
        font=dict(color=color, size=10),
        xanchor='left'
    )

# Update layout
fig.update_layout(
    title="Chicago Crime Database Schema",
    xaxis=dict(range=[0, 1], showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(range=[0, 1], showgrid=False, showticklabels=False, zeroline=False),
    plot_bgcolor='white',
    showlegend=False
)

# Save the chart
fig.write_image("chicago_crime_schema.png")
fig.write_image("chicago_crime_schema.svg", format="svg")

print("Database schema diagram created successfully!")