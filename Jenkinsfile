pipeline {
    agent any

    environment {
        BASE_URL = 'http://localhost:8000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                    echo "Setting up Python environment..."
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-html
                    pip install beautifulsoup4 requests Pillow
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    echo "Running tests..."
                    pytest -v --html=report.html --self-contained-html
                '''
            }
            post {
                always {
                    // 只发布 HTML 报告
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'report.html',
                        reportName: 'Test Report'
                    ])

                    // 存档测试日志
                    archiveArtifacts artifacts: 'report.html', fingerprint: true
                }
            }
        }
    }

    post {
        always {
            echo "构建状态: ${currentBuild.result}"
            echo "查看测试报告: ${env.BUILD_URL}HTML_Report/"
        }
        success {
            echo "✅ 所有 46 个测试通过！"
            emailext (
                subject: "SUCCESS: 测试通过 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "所有 46 个测试用例全部通过！\n查看报告: ${env.BUILD_URL}",
                to: "your-email@example.com"
            )
        }
        failure {
            echo "❌ 测试失败！"
        }
    }
}