# RCCT: Recursive Chain-of-Thought Processing Framework

RCCT (Recursive Chain-of-Thought) is a Java-based framework that implements advanced recursive thought processing with interactive visualization capabilities. The project demonstrates how computational models can implement cognitive structures through hierarchical thought representation, meta-cognition, and cross-domain integration.

![RCCT Visualization](https://via.placeholder.com/800x400?text=RCCT+Visualization)

## 🎯 Project Goals

The RCCT project aims to achieve several ambitious goals:

### Core Goals

1. **Recursive Thought Processing**
   - Implement computational models of recursive thought chains
   - Support thoughts about thoughts (meta-cognitive reflection)
   - Enable deep hierarchical thought structures with efficient traversal
   - Employ memoization to avoid redundant computation

2. **Cross-Domain Integration**
   - Bridge computational implementation with cognitive science models
   - Connect formal data structures with knowledge representation
   - Enable translation between different thought representation formats
   - Demonstrate isomorphisms between computational, cognitive, and representational domains

3. **Interactive Visualization**
   - Provide intuitive visual exploration of complex thought structures
   - Support real-time manipulation of thought hierarchies
   - Offer multiple visualization perspectives (overview, recursive, cross-domain)
   - Make abstract thought relationships tangible and explorable

4. **Knowledge Representation**
   - Formalize thought structures in multiple formats (Java objects, YAML, code)
   - Support self-reference and aliasing in thought networks
   - Enable rich metadata attachment for enhanced processing
   - Create a clean, intuitive API for thought manipulation

## 🚀 Getting Started

### Prerequisites

- Java 17 or higher
- Gradle 7.6+ (or use the included Gradle wrapper)
- Docker and Docker Compose (for containerized deployment)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/rcct.git
cd rcct

# Build and run with Gradle
./gradlew bootRun

# Alternatively, run with Docker
docker-compose up -d
```

Once running, access the application at:
- **Web Interface**: http://localhost:8080/api/visualization/
- **API**: http://localhost:8080/api/visualization/thoughts
- **H2 Console** (for development): http://localhost:8080/h2-console
  - JDBC URL: `jdbc:h2:mem:rcctdb`
  - Username: `sa`
  - Password: `password`

## 🏗️ Architecture

RCCT follows a layered architecture with clean separation of concerns:

### 1. Data Layer
- Entity models with JPA annotations
- H2 in-memory database (configurable for other databases)
- Repository interfaces for data access

### 2. Service Layer
- Business logic for thought processing
- Recursive evaluation algorithms
- Memoization implementation
- Cross-domain mapping utilities

### 3. API Layer
- RESTful endpoints for data access
- Thymeleaf templates for server-side rendering
- JSON serialization for programmatic access

### 4. Visualization Layer
- Interactive web interface with SVG visualization
- Dynamic tree structure rendering
- Multiple visualization perspectives

## 🧠 Key Concepts

### Thought Nodes
The fundamental units of the RCCT system are `ThoughtNode` objects, which represent discrete cognitive elements. Each node has:
- **Content**: The core thought content
- **Type**: Categorization (e.g., "concept", "question", "insight")
- **Depth**: Position in the recursive hierarchy
- **Parent**: Reference to the containing thought (if any)
- **Metadata**: Additional contextual information

### Recursive Processing
RCCT implements true recursive processing with:
- Self-referential thought structures
- Deep hierarchical traversal
- Memoization to avoid redundant computation
- Meta-cognitive reflection capabilities

### Integration Framework
The system provides integration across three domains:
- **Computational**: Java/Spring implementation
- **Cognitive**: Neural/cognitive process modeling
- **Representational**: YAML and other formal notations

## 🔧 Technologies

RCCT leverages several modern technologies:

- **Java 17**: For core implementation
- **Spring Boot 3.2.3**: Application framework
- **Spring Data JPA**: Database interaction
- **Jakarta Persistence**: Entity modeling
- **Lombok**: Boilerplate reduction
- **Thymeleaf**: Server-side templates
- **H2 Database**: In-memory data storage
- **Docker**: Containerization
- **SVG/JavaScript**: Visualization

## 📦 Docker Deployment

For easy deployment, RCCT provides Docker support:

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

The Docker setup includes:
- Multi-stage build for efficient image size
- Health checks for reliability
- Environment-specific configuration
- Exposed ports for easy access

## 📚 Resources

### Project Files

- `/src/main/java/com/anthropic/rcct/model/`: Data model classes
- `/src/main/java/com/anthropic/rcct/service/`: Business logic services
- `/src/main/java/com/anthropic/rcct/controller/`: API endpoints
- `/src/main/resources/templates/`: HTML templates
- `/src/main/resources/application.properties`: Configuration

### External Resources

- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Jakarta Persistence Documentation](https://jakarta.ee/specifications/persistence/)
- [Thymeleaf Documentation](https://www.thymeleaf.org/documentation.html)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Work

- Implement more sophisticated recursive evaluation strategies
- Add natural language processing capabilities
- Develop graph-based visualization alternatives
- Create integrations with external cognitive models
- Implement distributed processing for large thought networks