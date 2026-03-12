// Jenkinsfile
// SDD Validation Pipeline

pipeline {
    agent any
    
    environment {
        SDD_ROOT = "${WORKSPACE}"
        PYTHON_VERSION = '3.11'
    }
    
    stages {
        stage('Validate SDD') {
            steps {
                script {
                    def configFile = params.FAST_PATH ? 
                        'skills/sdd-orchestrator/validate-sdd.config.fast-path.json' :
                        'skills/sdd-orchestrator/validate-sdd.config.single-layer.json'
                    
                    sh "python${PYTHON_VERSION} skills/sdd-orchestrator/validate-sdd.py --config ${configFile}"
                }
            }
        }
        
        stage('Validate Content') {
            steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                        sh "python${PYTHON_VERSION} skills/sdd-orchestrator/validate-sdd.py --validate-content true"
                    }
                }
            }
        }
    }
    
    parameters {
        booleanParam(
            name: 'FAST_PATH',
            defaultValue: false,
            description: 'Use fast path validation for simple changes'
        )
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'docs/specs/**', fingerprint: true
        }
    }
}
