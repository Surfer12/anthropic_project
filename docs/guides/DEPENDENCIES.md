# RCCT: Recursive Chain-of-Thought Processing Framework

RCCT (Recursive Chain-of-Thought) is a Java-based framework that implements advanced recursive thought processing with interactive visualization capabilities.

## Fixing Dependency Issues

If you encounter issues with Jakarta Persistence or Lombok dependencies, follow these steps:

### 1. Ensure you have Java 17 installed

```bash
java -version
```

### 2. Verify Gradle is installed

```bash
./gradlew --version
```

### 3. Run the build verification script

```bash
./build-verify.sh
```

### 4. For IDE-specific issues:

#### IntelliJ IDEA:
1. Enable annotation processing:
   - Settings > Build, Execution, Deployment > Compiler > Annotation Processors
   - Check "Enable annotation processing"

2. Install the Lombok plugin:
   - Settings > Plugins > Marketplace
   - Search for "Lombok" and install

3. Refresh Gradle:
   - Open the Gradle tool window
   - Click the Refresh button

#### Eclipse:
1. Install the Lombok plugin:
   - Run `java -jar lombok-1.18.30.jar`
   - Follow the installation prompts

2. Update project configuration:
   - Right-click on the project > Properties
   - Java Compiler > Annotation Processing
   - Enable annotation processing

### 5. Manual dependency verification

Check if the required dependencies are on your classpath:

```bash
./gradlew -q dependencies | grep -E 'lombok|jakarta'
```

## Getting Started

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.