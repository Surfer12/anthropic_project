# RCCT User Guide

This comprehensive guide will help you understand, install, and use the Recursive Chain-of-Thought (RCCT) Framework.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Core Concepts](#core-concepts)
4. [Using the Visualization Interface](#using-the-visualization-interface)
5. [API Reference](#api-reference)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

## Introduction

The Recursive Chain-of-Thought (RCCT) Framework provides a computational model for recursive thought processing with interactive visualization. It enables researchers, cognitive scientists, and software engineers to:

- Model complex thought structures and their relationships
- Visualize hierarchical thought patterns
- Implement and test meta-cognitive processes
- Explore isomorphisms between computational, cognitive, and representational domains

RCCT is designed to be both a practical tool and a theoretical exploration of how recursive thinking can be modeled in software.

## Installation

### Method 1: Local Installation

#### Prerequisites

- Java Development Kit (JDK) 17 or higher
- Gradle 7.6+ (or use the included Gradle wrapper)
- Git (for cloning the repository)

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/rcct.git
   cd rcct
   ```

2. Build the project:
   ```bash
   ./gradlew build
   ```

3. Run the application:
   ```bash
   ./gradlew bootRun
   ```

4. Access the application in your browser:
   - Web Interface: [http://localhost:8080/api/visualization/](http://localhost:8080/api/visualization/)
   - API: [http://localhost:8080/api/visualization/thoughts](http://localhost:8080/api/visualization/thoughts)
   - H2 Console: [http://localhost:8080/h2-console](http://localhost:8080/h2-console)

### Method 2: Docker Installation

#### Prerequisites

- Docker
- Docker Compose

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/rcct.git
   cd rcct
   ```

2. Start with Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Access the application as described above.

## Core Concepts

Understanding these key concepts will help you make the most of the RCCT Framework.

### Thought Nodes

The fundamental unit in RCCT is the `ThoughtNode`, which represents a discrete thought or idea. Each thought node has:

- **ID**: Unique identifier
- **Content**: The actual thought content
- **Type**: Categorization (e.g., "concept", "question", "observation")
- **Depth**: Level in the thought hierarchy
- **Parent ID**: Reference to the containing thought
- **Metadata**: Additional contextual information

### CCT Models

The `CCTModel` acts as a container for related thought nodes, forming a complete thought structure. It includes:

- **ID**: Unique identifier
- **Name**: Descriptive name
- **Description**: Detailed explanation
- **Thoughts**: Collection of ThoughtNodes
- **Metadata**: Additional model properties

### Recursive Relationships

Thoughts in RCCT can have recursive relationships:

1. **Hierarchical**: Thoughts can contain sub-thoughts to any depth
2. **Self-referential**: Thoughts can refer to themselves (directly or indirectly)
3. **Cross-referential**: Thoughts can reference other thoughts across the model

### Meta-cognition

RCCT supports meta-cognition—thinking about thinking—through:

1. **Reflection**: Creating thoughts about existing thoughts
2. **Evaluation**: Assessing thought patterns and structures
3. **Transformation**: Modifying thought structures based on meta-level insights

## Using the Visualization Interface

The RCCT visualization interface provides an interactive way to explore thought structures.

### Navigation

The interface consists of three main sections:

1. **Thought Tree** (left panel): Hierarchical display of thought nodes
2. **Visualization Panel** (center panel): Interactive graphical representation
3. **Details Panel** (bottom panel): Information about selected thoughts

### Interacting with the Visualization

- **Select a Thought**: Click on any node in the thought tree or visualization
- **View Details**: After selecting a node, its details appear in the bottom panel
- **Switch Visualization**: Use the buttons above the visualization panel:
  - **Overview**: Shows the high-level structure
  - **Recursive Structure**: Focuses on recursive relationships
  - **Cross-Domain Integration**: Shows domain connections

### Tabs in the Details Panel

The Details Panel has three tabs:

1. **Details**: Shows the description of the selected thought
2. **YAML**: Presents the thought structure in YAML format
3. **Code**: Shows a Java code representation

## API Reference

RCCT provides a RESTful API for programmatic access.

### Endpoints

#### GET /api/visualization/

Returns the HTML visualization interface.

#### GET /api/visualization/thoughts

Returns a list of thought nodes in JSON format.

Example response:
```json
[
  {
    "id": 1,
    "content": "Sample thought",
    "type": "core",
    "depth": 0,
    "parentId": null,
    "metadata": null
  }
]
```

#### POST /api/visualization/thoughts

Creates a new thought node.

Request body:
```json
{
  "content": "New thought",
  "type": "concept",
  "depth": 1,
  "parentId": 1
}
```

### Using the API

Example with curl:
```bash
# Get all thoughts
curl -X GET http://localhost:8080/api/visualization/thoughts

# Create a new thought
curl -X POST http://localhost:8080/api/visualization/thoughts \
  -H "Content-Type: application/json" \
  -d '{"content":"New thought","type":"concept","depth":1,"parentId":1}'
```

## Advanced Usage

### Customizing the CCT Model

You can extend the default model by:

1. Creating custom thought types
2. Implementing specialized processing logic
3. Extending the visualization capabilities

Example service extension:
```java
@Service
public class CustomThoughtService extends ThoughtProcessingService {
    
    public ThoughtNode createSpecializedThought(String content, String specialProperty) {
        ThoughtNode thought = new ThoughtNode();
        thought.setContent(content);
        thought.setType("specialized");
        thought.setMetadata("{\"specialProperty\": \"" + specialProperty + "\"}");
        return thought;
    }
}
```

### Database Configuration

By default, RCCT uses an H2 in-memory database. For production use, you may want to configure a persistent database:

1. Add the appropriate database dependency to `build.gradle`
2. Update `application.properties` with your database configuration
3. Restart the application

Example MySQL configuration:
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/rcct
spring.datasource.username=username
spring.datasource.password=password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.jpa.database-platform=org.hibernate.dialect.MySQL8Dialect
spring.jpa.hibernate.ddl-auto=update
```

## Troubleshooting

### Common Issues

#### Application Won't Start

**Symptom**: Error messages during startup.

**Solutions**:
- Check Java version (must be 17+)
- Verify port 8080 is available
- Check database connectivity if using an external database

#### Visualization Not Loading

**Symptom**: Blank screen or error in browser console.

**Solutions**:
- Clear browser cache
- Check browser console for JavaScript errors
- Verify API endpoints are accessible

#### Docker Issues

**Symptom**: Docker container fails to start.

**Solutions**:
- Check Docker and Docker Compose installation
- Verify port mappings aren't conflicting
- Examine logs with `docker-compose logs rcct-app`

## FAQ

### General Questions

**Q: What is a Recursive Chain-of-Thought?**  
A: It's a computational model that represents how thoughts can build upon each other recursively, similar to how human cognition works with nested, self-referential thinking patterns.

**Q: Is RCCT a cognitive model or a software framework?**  
A: It's both! RCCT implements computational structures that model cognitive processes, bridging theoretical cognitive science with practical software implementation.

**Q: Can RCCT be used for AI research?**  
A: Yes, RCCT provides structures that can be valuable for researching recursive reasoning, meta-cognition, and hierarchical thought modeling in AI systems.

### Technical Questions

**Q: Does RCCT support distributed processing?**  
A: The current version runs in a single JVM, but future versions may support distributed processing for large thought networks.

**Q: Can I extend the visualization capabilities?**  
A: Yes, the visualization is built with standard web technologies (HTML, CSS, JavaScript, SVG) and can be extended or customized.

**Q: Is there a performance limit to the number of thought nodes?**  
A: The in-memory H2 database is suitable for hundreds of thousands of nodes. For larger-scale usage, configure a dedicated database server.

---

For additional support, please open an issue on the GitHub repository or contact the project maintainers.