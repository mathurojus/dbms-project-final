import plotly.graph_objects as go
import plotly.express as px

# Create a comprehensive system architecture diagram using Plotly
fig = go.Figure()

# Define colors for each component type
colors = {
    'datasource': '#B3E5EC',    # light blue
    'etl': '#A5D6A7',           # green  
    'database': '#FFE0B2',      # orange
    'ml': '#E1BEE7',            # purple
    'api': '#FFCDD2',           # red
    'frontend': '#B2DFDB',      # teal
    'external': '#FFEB8A',      # yellow
    'deployment': '#E0E0E0'     # gray
}

# Define component positions and details
components = [
    # Top section - Data Sources
    {'text': 'Kaggle Dataset', 'x': 0.15, 'y': 0.9, 'type': 'datasource', 'width': 120, 'height': 40},
    {'text': 'Chicago Data Portal API', 'x': 0.35, 'y': 0.9, 'type': 'datasource', 'width': 150, 'height': 40},
    
    # Middle-left - ETL Pipeline
    {'text': 'ETL Pipeline<br>download_data.py<br>clean_data.py<br>feature_engineering.py<br>load_to_mysql.py', 
     'x': 0.15, 'y': 0.7, 'type': 'etl', 'width': 200, 'height': 120},
    
    # Middle-center - Database
    {'text': 'MySQL 8.0<br>incidents table<br>grid_aggregates table<br>predictions table', 
     'x': 0.5, 'y': 0.6, 'type': 'database', 'width': 180, 'height': 100},
    
    # Middle-right - ML Training
    {'text': 'ML Training<br>train_model.py<br>LightGBM/XGBoost<br>SHAP Explainer', 
     'x': 0.8, 'y': 0.7, 'type': 'ml', 'width': 160, 'height': 100},
     
    # Trained Models
    {'text': 'Trained Models', 'x': 0.8, 'y': 0.5, 'type': 'ml', 'width': 120, 'height': 40},
    
    # Lower-middle - API Backend
    {'text': 'FastAPI Backend<br>/api/health<br>/api/grids/forecast<br>/api/grids/nearby<br>/api/historical<br>/api/explain', 
     'x': 0.5, 'y': 0.35, 'type': 'api', 'width': 180, 'height': 120},
    
    # Bottom - Frontend
    {'text': 'React + TypeScript Frontend<br>Dashboard page<br>HeatMap component (Mapbox)<br>TimeSeriesChart<br>PatrolPlanner<br>Analytics page', 
     'x': 0.5, 'y': 0.1, 'type': 'frontend', 'width': 220, 'height': 120},
    
    # Right side - External Services
    {'text': 'Mapbox GL JS', 'x': 0.85, 'y': 0.1, 'type': 'external', 'width': 100, 'height': 40},
    
    # Left side - Deployment
    {'text': 'Docker Compose<br>MySQL Container<br>API Container<br>Frontend Container', 
     'x': 0.1, 'y': 0.35, 'type': 'deployment', 'width': 150, 'height': 100}
]

# Add component boxes
for comp in components:
    fig.add_shape(
        type="rect",
        x0=comp['x'] - comp['width']/2000, y0=comp['y'] - comp['height']/2000,
        x1=comp['x'] + comp['width']/2000, y1=comp['y'] + comp['height']/2000,
        fillcolor=colors[comp['type']],
        line=dict(color="black", width=2),
        layer="below"
    )
    
    fig.add_annotation(
        text=comp['text'],
        x=comp['x'], y=comp['y'],
        showarrow=False,
        font=dict(size=9, color="black"),
        bgcolor="rgba(255,255,255,0)",
        borderwidth=0,
        align="center"
    )

# Define arrows showing data flow
arrows = [
    # Data Sources to ETL
    {'x0': 0.25, 'y0': 0.85, 'x1': 0.2, 'y1': 0.8, 'label': ''},
    
    # ETL to Database
    {'x0': 0.25, 'y0': 0.65, 'x1': 0.42, 'y1': 0.6, 'label': ''},
    
    # Database to ML Training
    {'x0': 0.58, 'y0': 0.65, 'x1': 0.72, 'y1': 0.7, 'label': ''},
    
    # ML Training to Trained Models
    {'x0': 0.8, 'y0': 0.65, 'x1': 0.8, 'y1': 0.55, 'label': ''},
    
    # Database to API (bidirectional)
    {'x0': 0.5, 'y0': 0.55, 'x1': 0.5, 'y1': 0.45, 'label': ''},
    
    # Trained Models to API
    {'x0': 0.75, 'y0': 0.5, 'x1': 0.58, 'y1': 0.4, 'label': ''},
    
    # API to Frontend
    {'x0': 0.5, 'y0': 0.25, 'x1': 0.5, 'y1': 0.2, 'label': ''},
    
    # Mapbox to Frontend
    {'x0': 0.8, 'y0': 0.1, 'x1': 0.65, 'y1': 0.1, 'label': ''},
    
    # Docker connections (dotted)
    {'x0': 0.18, 'y0': 0.4, 'x1': 0.42, 'y1': 0.55, 'label': '', 'style': 'dot'},
    {'x0': 0.18, 'y0': 0.35, 'x1': 0.42, 'y1': 0.35, 'label': '', 'style': 'dot'},
    {'x0': 0.18, 'y0': 0.3, 'x1': 0.42, 'y1': 0.2, 'label': '', 'style': 'dot'}
]

# Add arrows
for arrow in arrows:
    line_style = 'solid' if arrow.get('style') != 'dot' else 'dot'
    fig.add_annotation(
        x=arrow['x1'], y=arrow['y1'],
        ax=arrow['x0'], ay=arrow['y0'],
        xref="x", yref="y",
        axref="x", ayref="y",
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor="black",
        showarrow=True,
        text="",
        standoff=5,
        startstandoff=5
    )
    
    # Add dotted lines for Docker connections
    if arrow.get('style') == 'dot':
        fig.add_shape(
            type="line",
            x0=arrow['x0'], y0=arrow['y0'],
            x1=arrow['x1'], y1=arrow['y1'],
            line=dict(color="gray", width=2, dash="dot"),
            layer="below"
        )

# Create legend
legend_items = [
    {'label': 'Data Sources', 'color': colors['datasource']},
    {'label': 'ETL Pipeline', 'color': colors['etl']},
    {'label': 'Database', 'color': colors['database']},
    {'label': 'ML Training', 'color': colors['ml']},
    {'label': 'API Backend', 'color': colors['api']},
    {'label': 'Frontend', 'color': colors['frontend']},
    {'label': 'External Services', 'color': colors['external']},
    {'label': 'Deployment', 'color': colors['deployment']}
]

for i, item in enumerate(legend_items):
    fig.add_shape(
        type="rect",
        x0=0.02, y0=0.95 - i*0.04,
        x1=0.04, y1=0.93 - i*0.04,
        fillcolor=item['color'],
        line=dict(color="black", width=1),
        layer="above"
    )
    
    fig.add_annotation(
        text=item['label'],
        x=0.05, y=0.94 - i*0.04,
        showarrow=False,
        font=dict(size=8, color="black"),
        xanchor="left",
        yanchor="middle"
    )

# Update layout
fig.update_layout(
    title="Chicago Crimes Analytics System Architecture",
    xaxis=dict(range=[0, 1], showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(range=[0, 1], showgrid=False, showticklabels=False, zeroline=False),
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial", size=10)
)

# Remove axes
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

# Save as both PNG and SVG
fig.write_image("system_architecture.png")
fig.write_image("system_architecture.svg", format="svg")

print("System architecture diagram created successfully!")
print("Saved as: system_architecture.png and system_architecture.svg")