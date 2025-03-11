from utils.vector import DynamicVector
from utils.string import String

enum ProblemType:
    GENERAL = 0
    OPTIMIZATION = 1
    ANALYSIS = 2
    DESIGN = 3
    IMPLEMENTATION = 4

enum ProblemPriority:
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

struct Problem:
    var name: String
    var description: String
    var constraints: DynamicVector[String]
    var success_criteria: DynamicVector[String]
    var type: ProblemType
    var priority: ProblemPriority
    
    fn __init__(
        self,
        name: String,
        description: String,
        constraints: DynamicVector[String],
        success_criteria: DynamicVector[String],
        type: ProblemType = ProblemType.GENERAL,
        priority: ProblemPriority = ProblemPriority.MEDIUM
    ):
        self.name = name
        self.description = description
        self.constraints = constraints
        self.success_criteria = success_criteria
        self.type = type
        self.priority = priority
    
    fn is_valid(self) -> Bool:
        return (
            self.name.length() > 0 and
            self.description.length() > 0 and
            self.constraints.size() > 0 and
            self.success_criteria.size() > 0
        )
    
    fn is_high_priority(self) -> Bool:
        return (
            self.priority == ProblemPriority.HIGH or
            self.priority == ProblemPriority.CRITICAL
        )
    
    fn requires_optimization(self) -> Bool:
        if self.type == ProblemType.OPTIMIZATION:
            return True
            
        # Check constraints for optimization keywords
        for i in range(self.constraints.size()):
            let constraint = self.constraints[i].lower()
            if (
                constraint.contains("performance") or
                constraint.contains("optimize") or
                constraint.contains("efficiency")
            ):
                return True
        
        return False
    
    @staticmethod
    fn create_optimization_problem(
        name: String,
        description: String,
        constraints: DynamicVector[String],
        success_criteria: DynamicVector[String]
    ) -> Problem:
        return Problem(
            name=name,
            description=description,
            constraints=constraints,
            success_criteria=success_criteria,
            type=ProblemType.OPTIMIZATION,
            priority=ProblemPriority.HIGH
        ) 