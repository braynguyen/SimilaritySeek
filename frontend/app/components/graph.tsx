"use client"
import dynamic from 'next/dynamic';
import { useEffect, useState } from 'react';

// Dynamically import ForceGraph3D and disable SSR
const ForceGraph3D = dynamic(() => import('react-force-graph').then(mod => mod.ForceGraph3D), {
  ssr: false,
});

function Graph1() {
  const [graphData, setGraphData] = useState(null);

  useEffect(() => {
    // Fetch the graph data
    fetch('/data/graph1.json')
      .then(response => response.json())
      .then(data => setGraphData(data));
  }, []);

  if (!graphData) {
    return <div>Loading graph...</div>;
  }

  return (
    <div>
      <ForceGraph3D width={620} height={550} graphData={graphData} />
    </div>
  );
}

export default Graph1;
