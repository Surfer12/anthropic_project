from tensor import Tensor
from utils.vector import DynamicVector
from profiler.enhanced_profiler import KernelMetrics, HardwareMetrics, WorkloadMetrics
from math import sqrt, exp, sin, cos, pi

struct Color:
    var r: Float32
    var g: Float32
    var b: Float32
    var a: Float32
    
    fn __init__(inout self, r: Float32, g: Float32, b: Float32, a: Float32 = 1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

struct Point:
    var x: Float32
    var y: Float32
    
    fn __init__(inout self, x: Float32, y: Float32):
        self.x = x
        self.y = y

struct PerformanceGraph:
    var width: Int
    var height: Int
    var padding: Int
    var data: DynamicVector[Float32]
    var labels: DynamicVector[String]
    var colors: DynamicVector[Color]
    
    fn __init__(inout self, width: Int = 800, height: Int = 600, padding: Int = 50):
        self.width = width
        self.height = height
        self.padding = padding
        self.data = DynamicVector[Float32]()
        self.labels = DynamicVector[String]()
        self.colors = DynamicVector[Color]()
    
    fn add_data_point(inout self, value: Float32, label: String, color: Color):
        self.data.append(value)
        self.labels.append(label)
        self.colors.append(color)
    
    fn generate_svg(self) -> String:
        var svg = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">\n'
        
        # Add background
        svg += f'<rect width="{self.width}" height="{self.height}" fill="#f8f9fa"/>\n'
        
        # Draw axes
        svg += self._draw_axes()
        
        # Draw data
        svg += self._draw_data()
        
        # Draw labels
        svg += self._draw_labels()
        
        svg += "</svg>"
        return svg
    
    fn _draw_axes(self) -> String:
        var axes = ""
        
        # X-axis
        axes += f'<line x1="{self.padding}" y1="{self.height - self.padding}" '
        axes += f'x2="{self.width - self.padding}" y2="{self.height - self.padding}" '
        axes += 'stroke="black" stroke-width="2"/>\n'
        
        # Y-axis
        axes += f'<line x1="{self.padding}" y1="{self.padding}" '
        axes += f'x2="{self.padding}" y2="{self.height - self.padding}" '
        axes += 'stroke="black" stroke-width="2"/>\n'
        
        return axes
    
    fn _draw_data(self) -> String:
        var data_svg = ""
        let bar_width = (self.width - 2 * self.padding) / len(self.data)
        let scale = (self.height - 2 * self.padding) / 100.0  # Assuming percentage values
        
        for i in range(len(self.data)):
            let x = self.padding + i * bar_width
            let height = self.data[i] * scale
            let y = self.height - self.padding - height
            
            data_svg += f'<rect x="{x}" y="{y}" width="{bar_width * 0.8}" height="{height}" '
            data_svg += f'fill="rgba({self.colors[i].r * 255},{self.colors[i].g * 255},'
            data_svg += f'{self.colors[i].b * 255},{self.colors[i].a})" '
            data_svg += 'rx="5" ry="5"/>\n'
            
            # Add value label
            data_svg += f'<text x="{x + bar_width * 0.4}" y="{y - 5}" '
            data_svg += 'text-anchor="middle" font-size="12">'
            data_svg += f'{self.data[i]:.1f}%</text>\n'
        
        return data_svg
    
    fn _draw_labels(self) -> String:
        var labels_svg = ""
        let bar_width = (self.width - 2 * self.padding) / len(self.data)
        
        for i in range(len(self.labels)):
            let x = self.padding + i * bar_width + bar_width * 0.4
            let y = self.height - self.padding + 20
            
            labels_svg += f'<text x="{x}" y="{y}" text-anchor="middle" '
            labels_svg += f'transform="rotate(45,{x},{y})" font-size="12">'
            labels_svg += f'{self.labels[i]}</text>\n'
        
        return labels_svg

struct RadarChart:
    var width: Int
    var height: Int
    var metrics: DynamicVector[Float32]
    var labels: DynamicVector[String]
    var color: Color
    
    fn __init__(inout self, width: Int = 400, height: Int = 400):
        self.width = width
        self.height = height
        self.metrics = DynamicVector[Float32]()
        self.labels = DynamicVector[String]()
        self.color = Color(0.2, 0.6, 1.0, 0.5)
    
    fn add_metric(inout self, value: Float32, label: String):
        self.metrics.append(value)
        self.labels.append(label)
    
    fn generate_svg(self) -> String:
        var svg = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">\n'
        
        # Add background
        svg += f'<rect width="{self.width}" height="{self.height}" fill="#f8f9fa"/>\n'
        
        # Draw radar
        let center_x = self.width / 2
        let center_y = self.height / 2
        let radius = min(center_x, center_y) - 50
        
        # Draw background circles
        for i in range(1, 6):
            let r = radius * i / 5
            svg += f'<circle cx="{center_x}" cy="{center_y}" r="{r}" '
            svg += 'fill="none" stroke="#ddd" stroke-width="1"/>\n'
        
        # Draw axes
        let n = len(self.metrics)
        for i in range(n):
            let angle = 2 * pi * i / n
            let x = center_x + radius * cos(angle)
            let y = center_y + radius * sin(angle)
            
            svg += f'<line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}" '
            svg += 'stroke="#ddd" stroke-width="1"/>\n'
            
            # Add label
            let label_x = center_x + (radius + 20) * cos(angle)
            let label_y = center_y + (radius + 20) * sin(angle)
            svg += f'<text x="{label_x}" y="{label_y}" text-anchor="middle" '
            svg += f'alignment-baseline="middle" font-size="12">{self.labels[i]}</text>\n'
        
        # Draw data polygon
        var points = ""
        for i in range(n):
            let angle = 2 * pi * i / n
            let r = radius * self.metrics[i]
            let x = center_x + r * cos(angle)
            let y = center_y + r * sin(angle)
            points += f"{x},{y} "
        
        svg += f'<polygon points="{points}" fill="rgba({self.color.r * 255},'
        svg += f'{self.color.g * 255},{self.color.b * 255},{self.color.a})" '
        svg += 'stroke="rgba(0,0,0,0.5)" stroke-width="2"/>\n'
        
        svg += "</svg>"
        return svg

@value
struct PerformanceVisualizer:
    fn visualize_kernel_metrics(metrics: KernelMetrics) -> String:
        var html = "<html><body style='font-family: Arial, sans-serif;'>\n"
        
        # Create performance graph
        var perf_graph = PerformanceGraph()
        perf_graph.add_data_point(metrics.calculate_efficiency() * 100, 
                                "Compute Efficiency", 
                                Color(0.2, 0.6, 1.0))
        perf_graph.add_data_point(metrics.calculate_memory_efficiency() * 100,
                                "Memory Efficiency",
                                Color(0.2, 1.0, 0.6))
        perf_graph.add_data_point(metrics.workload.simd_efficiency * 100,
                                "SIMD Efficiency",
                                Color(1.0, 0.6, 0.2))
        perf_graph.add_data_point(metrics.workload.thread_occupancy * 100,
                                "Thread Occupancy",
                                Color(0.6, 0.2, 1.0))
        
        html += "<h2>Performance Metrics</h2>\n"
        html += perf_graph.generate_svg()
        
        # Create hardware metrics radar chart
        var hw_chart = RadarChart()
        hw_chart.add_metric(metrics.hardware.gpu_utilization, "GPU Util")
        hw_chart.add_metric(metrics.hardware.memory_bandwidth / 400.0, "Memory BW")
        hw_chart.add_metric(metrics.hardware.cache_hit_rate, "Cache Hits")
        hw_chart.add_metric(metrics.hardware.power_consumption / 100.0, "Power")
        hw_chart.add_metric(1.0 - metrics.hardware.temperature / 100.0, "Temp")
        
        html += "<h2>Hardware Metrics</h2>\n"
        html += hw_chart.generate_svg()
        
        html += "</body></html>"
        return html
    
    fn generate_report(metrics: DynamicVector[KernelMetrics]) -> String:
        var html = "<html><body style='font-family: Arial, sans-serif;'>\n"
        html += "<h1>Performance Analysis Report</h1>\n"
        
        # Overall performance graph
        var overall_graph = PerformanceGraph(width=1000)
        for i in range(len(metrics)):
            let metric = metrics[i]
            overall_graph.add_data_point(
                metric.calculate_efficiency() * 100,
                metric.name,
                Color(0.2 + 0.6 * i / len(metrics), 0.6, 1.0)
            )
        
        html += "<h2>Overall Kernel Performance</h2>\n"
        html += overall_graph.generate_svg()
        
        # Individual kernel details
        for metric in metrics:
            html += f"<h2>Kernel: {metric.name}</h2>\n"
            html += "<div style='display: flex;'>\n"
            
            # Performance metrics
            var perf_graph = PerformanceGraph(width=400)
            perf_graph.add_data_point(metric.calculate_efficiency() * 100,
                                    "Compute",
                                    Color(0.2, 0.6, 1.0))
            perf_graph.add_data_point(metric.calculate_memory_efficiency() * 100,
                                    "Memory",
                                    Color(0.2, 1.0, 0.6))
            perf_graph.add_data_point(metric.workload.simd_efficiency * 100,
                                    "SIMD",
                                    Color(1.0, 0.6, 0.2))
            html += perf_graph.generate_svg()
            
            # Hardware metrics
            var hw_chart = RadarChart()
            hw_chart.add_metric(metric.hardware.gpu_utilization, "GPU")
            hw_chart.add_metric(metric.hardware.memory_bandwidth / 400.0, "Mem")
            hw_chart.add_metric(metric.hardware.cache_hit_rate, "Cache")
            hw_chart.add_metric(metric.hardware.power_consumption / 100.0, "Power")
            hw_chart.add_metric(1.0 - metric.hardware.temperature / 100.0, "Temp")
            html += hw_chart.generate_svg()
            
            html += "</div>\n"
        
        html += "</body></html>"
        return html 