const { useState, useEffect, useRef } = React;

// Lucide Icons as SVG components
const Icons = {
  Home: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
      <polyline points="9 22 9 12 15 12 15 22"/>
    </svg>
  ),
  Shield: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  ),
  BarChart3: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 3v18h18"/>
      <path d="M18 17V9"/>
      <path d="M13 17V5"/>
      <path d="M8 17v-3"/>
    </svg>
  ),
  TrendingUp: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
      <polyline points="17 6 23 6 23 12"/>
    </svg>
  ),
  TrendingDown: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/>
      <polyline points="17 18 23 18 23 12"/>
    </svg>
  ),
  AlertCircle: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/>
      <line x1="12" y1="8" x2="12" y2="12"/>
      <line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
  ),
  MapPin: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
      <circle cx="12" cy="10" r="3"/>
    </svg>
  ),
  Clock: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/>
      <polyline points="12 6 12 12 16 14"/>
    </svg>
  ),
  Sun: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="5"/>
      <line x1="12" y1="1" x2="12" y2="3"/>
      <line x1="12" y1="21" x2="12" y2="23"/>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
      <line x1="1" y1="12" x2="3" y2="12"/>
      <line x1="21" y1="12" x2="23" y2="12"/>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
    </svg>
  ),
  Moon: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
    </svg>
  ),
  Bell: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
      <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
    </svg>
  ),
  Menu: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="3" y1="12" x2="21" y2="12"/>
      <line x1="3" y1="6" x2="21" y2="6"/>
      <line x1="3" y1="18" x2="21" y2="18"/>
    </svg>
  ),
  X: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18"/>
      <line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
  )
};

// Data
const crimeData = {
  stats: {
    totalCrimes: 45829,
    totalZones: 1247,
    crimeTypes: 34,
    arrestRate: 28.4
  },
  hourlyDistribution: [
    { hour: 0, crimes: 185, arrests: 42 },
    { hour: 1, crimes: 192, arrests: 38 },
    { hour: 2, crimes: 198, arrests: 35 },
    { hour: 3, crimes: 156, arrests: 28 },
    { hour: 4, crimes: 89, arrests: 12 },
    { hour: 5, crimes: 67, arrests: 8 },
    { hour: 6, crimes: 92, arrests: 15 },
    { hour: 7, crimes: 134, arrests: 25 },
    { hour: 8, crimes: 167, arrests: 32 },
    { hour: 9, crimes: 201, arrests: 45 },
    { hour: 10, crimes: 223, arrests: 52 },
    { hour: 11, crimes: 245, arrests: 58 },
    { hour: 12, crimes: 267, arrests: 64 },
    { hour: 13, crimes: 289, arrests: 70 },
    { hour: 14, crimes: 276, arrests: 68 },
    { hour: 15, crimes: 234, arrests: 56 },
    { hour: 16, crimes: 198, arrests: 48 },
    { hour: 17, crimes: 176, arrests: 42 },
    { hour: 18, crimes: 154, arrests: 38 },
    { hour: 19, crimes: 167, arrests: 40 },
    { hour: 20, crimes: 198, arrests: 48 },
    { hour: 21, crimes: 212, arrests: 52 },
    { hour: 22, crimes: 234, arrests: 58 },
    { hour: 23, crimes: 201, arrests: 48 }
  ],
  topCrimes: [
    { type: 'THEFT', count: 8934, percentage: 19.5 },
    { type: 'BATTERY', count: 6234, percentage: 13.6 },
    { type: 'CRIMINAL DAMAGE', count: 4567, percentage: 10.0 },
    { type: 'BURGLARY', count: 3892, percentage: 8.5 },
    { type: 'MOTOR VEHICLE THEFT', count: 3245, percentage: 7.1 },
    { type: 'ROBBERY', count: 2876, percentage: 6.3 },
    { type: 'NARCOTICS', count: 2654, percentage: 5.8 },
    { type: 'ASSAULT', count: 2345, percentage: 5.1 }
  ],
  patrolZones: [
    { gridId: 'dp3wmk', riskScore: 87, crimeCount: 432, location: [41.8821, -87.6298], crimeTypes: ['THEFT', 'BATTERY', 'ROBBERY'], recommendedHours: [20, 21, 22, 23, 0, 1, 2] },
    { gridId: 'dp3wml', riskScore: 76, crimeCount: 378, location: [41.8741, -87.6298], crimeTypes: ['THEFT', 'CRIMINAL DAMAGE'], recommendedHours: [21, 22, 23, 0, 1] },
    { gridId: 'dp3wmp', riskScore: 82, crimeCount: 405, location: [41.8801, -87.6308], crimeTypes: ['BATTERY', 'ROBBERY', 'NARCOTICS'], recommendedHours: [19, 20, 21, 22, 23, 0] },
    { gridId: 'dp3wmn', riskScore: 65, crimeCount: 298, location: [41.8761, -87.6288], crimeTypes: ['THEFT', 'BURGLARY'], recommendedHours: [20, 21, 22, 23] },
    { gridId: 'dp3wmo', riskScore: 71, crimeCount: 326, location: [41.8811, -87.6318], crimeTypes: ['CRIMINAL DAMAGE', 'MOTOR VEHICLE THEFT'], recommendedHours: [18, 19, 20, 21, 22] },
    { gridId: 'dp3wmq', riskScore: 58, crimeCount: 267, location: [41.8731, -87.6278], crimeTypes: ['THEFT'], recommendedHours: [20, 21, 22] },
    { gridId: 'dp3wmr', riskScore: 79, crimeCount: 389, location: [41.8791, -87.6328], crimeTypes: ['BATTERY', 'ROBBERY', 'THEFT'], recommendedHours: [19, 20, 21, 22, 23, 0, 1] },
    { gridId: 'dp3wms', riskScore: 53, crimeCount: 234, location: [41.8751, -87.6308], crimeTypes: ['NARCOTICS', 'ASSAULT'], recommendedHours: [21, 22, 23] }
  ],
  heatmapZones: [
    { zone: 'downtown', lat: 41.8781, lon: -87.6298, intensity: 0.95 },
    { zone: 'north_side', lat: 41.9200, lon: -87.6400, intensity: 0.72 },
    { zone: 'south_side', lat: 41.7900, lon: -87.6200, intensity: 0.68 },
    { zone: 'west_side', lat: 41.8500, lon: -87.7000, intensity: 0.81 },
    { zone: 'northwest', lat: 41.9500, lon: -87.7500, intensity: 0.45 }
  ]
};

// Stat Card Component
const StatCard = ({ title, value, trend, icon, darkMode }) => {
  const isPositive = trend > 0;
  const bgColor = darkMode ? 'bg-gray-800' : 'bg-white';
  const textColor = darkMode ? 'text-gray-200' : 'text-gray-900';
  const subTextColor = darkMode ? 'text-gray-400' : 'text-gray-600';
  
  return (
    <div className={`stat-card ${bgColor} rounded-lg p-6 shadow-lg border ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <p className={`text-sm font-medium ${subTextColor}`}>{title}</p>
          <p className={`text-3xl font-bold mt-2 ${textColor}`}>{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${darkMode ? 'bg-blue-900/30' : 'bg-blue-100'}`}>
          <div className="text-blue-500">{icon}</div>
        </div>
      </div>
      {trend !== undefined && (
        <div className="flex items-center mt-4">
          <span className={`flex items-center text-sm font-medium ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
            {isPositive ? <Icons.TrendingUp /> : <Icons.TrendingDown />}
            <span className="ml-1">{Math.abs(trend)}%</span>
          </span>
          <span className={`text-sm ml-2 ${subTextColor}`}>vs last month</span>
        </div>
      )}
    </div>
  );
};

// Map Visualization Component
const MapVisualization = ({ darkMode }) => {
  const getColorFromIntensity = (intensity) => {
    if (intensity >= 0.8) return '#EF4444'; // High - Red
    if (intensity >= 0.6) return '#F59E0B'; // Medium-High - Orange
    if (intensity >= 0.4) return '#EAB308'; // Medium - Yellow
    return '#10B981'; // Low - Green
  };

  return (
    <div className={`map-container ${darkMode ? 'bg-gray-800' : 'bg-gray-100'} relative`}>
      <svg width="100%" height="100%" viewBox="0 0 600 400" className="absolute inset-0">
        {/* Chicago base map outline */}
        <rect x="0" y="0" width="600" height="400" fill={darkMode ? '#1F2937' : '#F3F4F6'} />
        
        {/* Grid lines */}
        {[...Array(10)].map((_, i) => (
          <line key={`h${i}`} x1="0" y1={i * 40} x2="600" y2={i * 40} stroke={darkMode ? '#374151' : '#E5E7EB'} strokeWidth="1" />
        ))}
        {[...Array(15)].map((_, i) => (
          <line key={`v${i}`} x1={i * 40} y1="0" x2={i * 40} y2="400" stroke={darkMode ? '#374151' : '#E5E7EB'} strokeWidth="1" />
        ))}

        {/* Chicago label */}
        <text x="300" y="30" textAnchor="middle" fill={darkMode ? '#9CA3AF' : '#6B7280'} fontSize="14" fontWeight="600">
          Chicago Crime Heatmap
        </text>

        {/* Heatmap zones */}
        {crimeData.heatmapZones.map((zone, idx) => {
          // Convert lat/lon to SVG coordinates (simplified projection)
          const x = ((zone.lon + 87.7500) / (87.6200 - 87.7500)) * 600;
          const y = ((41.9500 - zone.lat) / (41.9500 - 41.7900)) * 400;
          const radius = 40 + zone.intensity * 40;
          const color = getColorFromIntensity(zone.intensity);
          
          return (
            <g key={idx} className="heatmap-marker">
              <circle
                cx={x}
                cy={y}
                r={radius}
                fill={color}
                opacity="0.15"
              />
              <circle
                cx={x}
                cy={y}
                r={radius * 0.6}
                fill={color}
                opacity="0.25"
              />
              <circle
                cx={x}
                cy={y}
                r={radius * 0.3}
                fill={color}
                opacity="0.4"
              />
              <circle
                cx={x}
                cy={y}
                r="8"
                fill={color}
              />
              <text
                x={x}
                y={y + radius + 15}
                textAnchor="middle"
                fill={darkMode ? '#E5E7EB' : '#374151'}
                fontSize="11"
                fontWeight="500"
              >
                {zone.zone.replace('_', ' ')}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Legend */}
      <div className={`absolute bottom-4 right-4 ${darkMode ? 'bg-gray-900/90' : 'bg-white/90'} backdrop-blur-sm rounded-lg p-3 shadow-lg`}>
        <div className="text-xs font-semibold mb-2" style={{ color: darkMode ? '#E5E7EB' : '#374151' }}>Crime Intensity</div>
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded" style={{ backgroundColor: '#EF4444' }}></div>
            <span className="text-xs" style={{ color: darkMode ? '#D1D5DB' : '#6B7280' }}>High (80%+)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded" style={{ backgroundColor: '#F59E0B' }}></div>
            <span className="text-xs" style={{ color: darkMode ? '#D1D5DB' : '#6B7280' }}>Med-High (60-80%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded" style={{ backgroundColor: '#EAB308' }}></div>
            <span className="text-xs" style={{ color: darkMode ? '#D1D5DB' : '#6B7280' }}>Medium (40-60%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded" style={{ backgroundColor: '#10B981' }}></div>
            <span className="text-xs" style={{ color: darkMode ? '#D1D5DB' : '#6B7280' }}>Low (&lt;40%)</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Time Series Chart Component
const TimeSeriesChart = ({ darkMode }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (chartRef.current) {
      const ctx = chartRef.current.getContext('2d');
      
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      chartInstance.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: crimeData.hourlyDistribution.map(d => d.hour + ':00'),
          datasets: [
            {
              label: 'Crimes',
              data: crimeData.hourlyDistribution.map(d => d.crimes),
              borderColor: '#3B82F6',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              tension: 0.4,
              fill: true
            },
            {
              label: 'Arrests',
              data: crimeData.hourlyDistribution.map(d => d.arrests),
              borderColor: '#10B981',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              tension: 0.4,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                color: darkMode ? '#E5E7EB' : '#374151',
                font: { size: 12 }
              }
            },
            tooltip: {
              mode: 'index',
              intersect: false
            }
          },
          scales: {
            x: {
              grid: {
                color: darkMode ? '#374151' : '#E5E7EB'
              },
              ticks: {
                color: darkMode ? '#9CA3AF' : '#6B7280'
              }
            },
            y: {
              grid: {
                color: darkMode ? '#374151' : '#E5E7EB'
              },
              ticks: {
                color: darkMode ? '#9CA3AF' : '#6B7280'
              }
            }
          }
        }
      });
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [darkMode]);

  return (
    <div className="chart-container">
      <canvas ref={chartRef}></canvas>
    </div>
  );
};

// Patrol Card Component
const PatrolCard = ({ zone, darkMode }) => {
  const getRiskColor = (score) => {
    if (score >= 80) return 'bg-red-500';
    if (score >= 60) return 'bg-orange-500';
    if (score >= 40) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const getRiskLabel = (score) => {
    if (score >= 80) return 'High Risk';
    if (score >= 60) return 'Medium-High';
    if (score >= 40) return 'Medium';
    return 'Low Risk';
  };

  const bgColor = darkMode ? 'bg-gray-800' : 'bg-white';
  const textColor = darkMode ? 'text-gray-200' : 'text-gray-900';
  const subTextColor = darkMode ? 'text-gray-400' : 'text-gray-600';

  return (
    <div className={`patrol-card ${bgColor} rounded-lg p-6 shadow-lg border ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className={`text-lg font-bold ${textColor}`}>Grid {zone.gridId}</h3>
          <p className={`text-sm ${subTextColor} flex items-center gap-1 mt-1`}>
            <Icons.MapPin />
            {zone.location[0].toFixed(4)}, {zone.location[1].toFixed(4)}
          </p>
        </div>
        <div className="text-right">
          <div className={`inline-flex items-center px-3 py-1 rounded-full text-white text-sm font-semibold ${getRiskColor(zone.riskScore)}`}>
            {zone.riskScore}
          </div>
          <p className={`text-xs ${subTextColor} mt-1`}>{getRiskLabel(zone.riskScore)}</p>
        </div>
      </div>

      <div className="mb-4">
        <p className={`text-sm font-medium ${subTextColor} mb-2`}>Crime Types:</p>
        <div className="flex flex-wrap gap-2">
          {zone.crimeTypes.map((type, idx) => (
            <span key={idx} className={`px-2 py-1 rounded text-xs font-medium ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'}`}>
              {type}
            </span>
          ))}
        </div>
      </div>

      <div className="mb-4">
        <p className={`text-sm font-medium ${subTextColor} mb-2 flex items-center gap-1`}>
          <Icons.Clock />
          Recommended Patrol Hours:
        </p>
        <div className="flex flex-wrap gap-1">
          {zone.recommendedHours.map((hour, idx) => (
            <span key={idx} className="px-2 py-1 rounded bg-blue-500 text-white text-xs font-medium">
              {hour}:00
            </span>
          ))}
        </div>
      </div>

      <div className={`flex justify-between items-center pt-4 border-t ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <span className={`text-sm ${subTextColor}`}>{zone.crimeCount} crimes reported</span>
        <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm font-medium transition-colors">
          View Details
        </button>
      </div>
    </div>
  );
};

// Dashboard Page
const Dashboard = ({ darkMode }) => {
  const textColor = darkMode ? 'text-gray-200' : 'text-gray-900';
  const subTextColor = darkMode ? 'text-gray-400' : 'text-gray-600';

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className={`text-3xl font-bold ${textColor}`}>Crime Analytics Dashboard</h1>
        <p className={`${subTextColor} mt-2`}>Real-time crime monitoring and analytics for Chicago</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Crimes"
          value={crimeData.stats.totalCrimes.toLocaleString()}
          trend={2.5}
          icon={<Icons.AlertCircle />}
          darkMode={darkMode}
        />
        <StatCard
          title="Active Zones"
          value={crimeData.stats.totalZones.toLocaleString()}
          trend={5.2}
          icon={<Icons.MapPin />}
          darkMode={darkMode}
        />
        <StatCard
          title="Crime Types"
          value={crimeData.stats.crimeTypes}
          icon={<Icons.BarChart3 />}
          darkMode={darkMode}
        />
        <StatCard
          title="Arrest Rate"
          value={crimeData.stats.arrestRate + '%'}
          trend={-1.2}
          icon={<Icons.Shield />}
          darkMode={darkMode}
        />
      </div>

      {/* Map and Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg p-6 shadow-lg border ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
          <h2 className={`text-xl font-bold mb-4 ${textColor}`}>Crime Hotspot Map</h2>
          <MapVisualization darkMode={darkMode} />
        </div>

        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg p-6 shadow-lg border ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
          <h2 className={`text-xl font-bold mb-4 ${textColor}`}>Hourly Crime Patterns</h2>
          <TimeSeriesChart darkMode={darkMode} />
        </div>
      </div>
    </div>
  );
};

// Patrol Planner Page
const PatrolPlanner = ({ darkMode }) => {
  const [sortBy, setSortBy] = useState('risk');
  const textColor = darkMode ? 'text-gray-200' : 'text-gray-900';
  const subTextColor = darkMode ? 'text-gray-400' : 'text-gray-600';

  const sortedZones = [...crimeData.patrolZones].sort((a, b) => {
    if (sortBy === 'risk') return b.riskScore - a.riskScore;
    return b.crimeCount - a.crimeCount;
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className={`text-3xl font-bold ${textColor}`}>Patrol Planner</h1>
        <p className={`${subTextColor} mt-2`}>Optimized patrol recommendations based on crime patterns</p>
      </div>

      {/* Filters */}
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg p-4 shadow-lg border ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <div className="flex flex-wrap gap-4 items-center">
          <div>
            <label className={`text-sm font-medium ${subTextColor} block mb-2`}>Sort By:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className={`px-4 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600 text-gray-200' : 'bg-white border-gray-300 text-gray-900'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
            >
              <option value="risk">Risk Score</option>
              <option value="crimes">Crime Count</option>
            </select>
          </div>
          <div>
            <label className={`text-sm font-medium ${subTextColor} block mb-2`}>Date Range:</label>
            <input
              type="date"
              className={`px-4 py-2 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600 text-gray-200' : 'bg-white border-gray-300 text-gray-900'} focus:outline-none focus:ring-2 focus:ring-blue-500`}
              defaultValue="2025-11-02"
            />
          </div>
        </div>
      </div>

      {/* Patrol Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {sortedZones.map((zone, idx) => (
          <PatrolCard key={idx} zone={zone} darkMode={darkMode} />
        ))}
      </div>
    </div>
  );
};

// Analytics Page
const Analytics = ({ darkMode }) => {
  const chartRef = useRef(null);
  const pieChartRef = useRef(null);
  const chartInstance = useRef(null);
  const pieChartInstance = useRef(null);
  const textColor = darkMode ? 'text-gray-200' : 'text-gray-900';
  const subTextColor = darkMode ? 'text-gray-400' : 'text-gray-600';

  useEffect(() => {
    // Bar chart for crime types
    if (chartRef.current) {
      const ctx = chartRef.current.getContext('2d');
      
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      chartInstance.current = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: crimeData.topCrimes.map(c => c.type),
          datasets: [{
            label: 'Crime Count',
            data: crimeData.topCrimes.map(c => c.count),
            backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F', '#DB4545', '#D2BA4C', '#964325']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            x: {
              grid: {
                color: darkMode ? '#374151' : '#E5E7EB'
              },
              ticks: {
                color: darkMode ? '#9CA3AF' : '#6B7280',
                font: { size: 10 }
              }
            },
            y: {
              grid: {
                color: darkMode ? '#374151' : '#E5E7EB'
              },
              ticks: {
                color: darkMode ? '#9CA3AF' : '#6B7280'
              }
            }
          }
        }
      });
    }

    // Pie chart for crime distribution
    if (pieChartRef.current) {
      const ctx = pieChartRef.current.getContext('2d');
      
      if (pieChartInstance.current) {
        pieChartInstance.current.destroy();
      }

      pieChartInstance.current = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: crimeData.topCrimes.map(c => c.type),
          datasets: [{
            data: crimeData.topCrimes.map(c => c.percentage),
            backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F', '#DB4545', '#D2BA4C', '#964325']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'right',
              labels: {
                color: darkMode ? '#E5E7EB' : '#374151',
                font: { size: 11 },
                padding: 10
              }
            }
          }
        }
      });
    }

    return () => {
      if (chartInstance.current) chartInstance.current.destroy();
      if (pieChartInstance.current) pieChartInstance.current.destroy();
    };
  }, [darkMode]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className={`text-3xl font-bold ${textColor}`}>Crime Analytics</h1>
        <p className={`${subTextColor} mt-2`}>Detailed breakdown and trends analysis</p>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg p-6 shadow-lg border ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
          <h2 className={`text-xl font-bold mb-4 ${textColor}`}>Crime Types Distribution</h2>
          <div className="chart-container">
            <canvas ref={chartRef}></canvas>
          </div>
        </div>

        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg p-6 shadow-lg border ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
          <h2 className={`text-xl font-bold mb-4 ${textColor}`}>Crime Percentage Breakdown</h2>
          <div className="chart-container">
            <canvas ref={pieChartRef}></canvas>
          </div>
        </div>
      </div>

      {/* Top Crimes List */}
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg p-6 shadow-lg border ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <h2 className={`text-xl font-bold mb-4 ${textColor}`}>Top Crime Types</h2>
        <div className="space-y-3">
          {crimeData.topCrimes.map((crime, idx) => (
            <div key={idx} className="flex items-center justify-between">
              <div className="flex items-center gap-3 flex-1">
                <span className={`text-2xl font-bold ${subTextColor}`}>{idx + 1}</span>
                <div className="flex-1">
                  <p className={`font-semibold ${textColor}`}>{crime.type}</p>
                  <div className="w-full bg-gray-700 rounded-full h-2 mt-1">
                    <div
                      className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${crime.percentage * 5}%` }}
                    ></div>
                  </div>
                </div>
              </div>
              <div className="text-right ml-4">
                <p className={`text-lg font-bold ${textColor}`}>{crime.count.toLocaleString()}</p>
                <p className={`text-sm ${subTextColor}`}>{crime.percentage}%</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Header Component
const Header = ({ darkMode, toggleTheme }) => {
  return (
    <header className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-b px-6 py-4 flex justify-between items-center`}>
      <div>
        <h1 className={`text-xl font-bold ${darkMode ? 'text-gray-200' : 'text-gray-900'}`}>Chicago Crime Analytics</h1>
      </div>
      <div className="flex items-center gap-4">
        <button
          onClick={toggleTheme}
          className={`p-2 rounded-lg ${darkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-100 hover:bg-gray-200'} transition-colors`}
          aria-label="Toggle theme"
        >
          {darkMode ? <Icons.Sun /> : <Icons.Moon />}
        </button>
        <button
          className={`p-2 rounded-lg ${darkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-100 hover:bg-gray-200'} transition-colors relative`}
          aria-label="Notifications"
        >
          <Icons.Bell />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
      </div>
    </header>
  );
};

// Sidebar Component
const Sidebar = ({ currentPage, setCurrentPage, darkMode, isOpen, setIsOpen }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <Icons.Home /> },
    { id: 'patrol', label: 'Patrol Planner', icon: <Icons.Shield /> },
    { id: 'analytics', label: 'Analytics', icon: <Icons.BarChart3 /> }
  ];

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setIsOpen(false)}
        ></div>
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-50 w-64 ${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-r transform transition-transform duration-300 ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}
      >
        <div className="p-6">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-500 rounded-lg">
                <Icons.Shield />
              </div>
              <span className={`text-lg font-bold ${darkMode ? 'text-gray-200' : 'text-gray-900'}`}>CPD</span>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="lg:hidden p-2 rounded-lg hover:bg-gray-700"
            >
              <Icons.X />
            </button>
          </div>

          <nav className="space-y-2">
            {menuItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  setCurrentPage(item.id);
                  setIsOpen(false);
                }}
                className={`sidebar-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left ${currentPage === item.id ? 'active' : ''} ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}
              >
                {item.icon}
                <span className="font-medium">{item.label}</span>
              </button>
            ))}
          </nav>
        </div>
      </aside>
    </>
  );
};

// Main App Component
const App = () => {
  const [darkMode, setDarkMode] = useState(true);
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleTheme = () => setDarkMode(!darkMode);

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard darkMode={darkMode} />;
      case 'patrol':
        return <PatrolPlanner darkMode={darkMode} />;
      case 'analytics':
        return <Analytics darkMode={darkMode} />;
      default:
        return <Dashboard darkMode={darkMode} />;
    }
  };

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
        <div className="flex">
          <Sidebar
            currentPage={currentPage}
            setCurrentPage={setCurrentPage}
            darkMode={darkMode}
            isOpen={sidebarOpen}
            setIsOpen={setSidebarOpen}
          />

          <div className="flex-1 flex flex-col min-h-screen">
            {/* Mobile menu button */}
            <div className={`lg:hidden ${darkMode ? 'bg-gray-800' : 'bg-white'} p-4 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
              <button
                onClick={() => setSidebarOpen(true)}
                className={`p-2 rounded-lg ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}`}
              >
                <Icons.Menu />
              </button>
            </div>

            <Header darkMode={darkMode} toggleTheme={toggleTheme} />

            <main className="flex-1 p-6 overflow-auto">
              {renderPage()}
            </main>
          </div>
        </div>
      </div>
    </div>
  );
};

// Render App
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);