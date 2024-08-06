import React from 'react';
import Plot from 'react-plotly.js';

const LineChart = ({ time, price, title }) => {
    return (
        <Plot 
            data={[
                {
                    x: time,
                    y: price,
                    type: 'scatter',
                    mode: 'lines+markers',
                    marker: {color: 'white', size: 8},
                },
            ]}
            layout={{
                title: {text: title,
                        font: {color: 'white'}},
                paper_bgcolor: '#282c34',
                plot_bgcolor: '#282c34',
                xaxis: {
                    title: {text: 'Time',
                            font: {color: 'white'}},
                    tickfont: {color: 'white'},
                    gridcolor: '#444'},
                yaxis: {
                    title: {text: 'Price',
                            font: {color: 'white'}},
                    tickfont: {color: 'white'},
                    gridcolor: '#444'},
            }}
            config={{
                displayModeBar: false,
                scrollZoom: false
            }}
            style={{width: '100%', height: '100%'}}
        />
    );
};

export default LineChart;