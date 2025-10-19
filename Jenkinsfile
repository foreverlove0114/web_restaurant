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
                    echo "Installing dependencies..."
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest allure-pytest pytest-html
                    # 安装测试所需的额外依赖
                    pip install beautifulsoup4 requests Pillow
                    echo "Dependencies installed successfully!"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    echo "Installed packages:"
                    pip list
                    echo "Running tests..."
                    pytest -v --alluredir=allure-results --html=pytest-report.html --self-contained-html
                '''
            }
            post {
                always {
                    // 保存 Allure 报告
                    allure includeProperties: false,
                          jdk: '',
                          results: [[path: 'allure-results']]
                    // 保存 HTML 报告
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'pytest-report.html',
                        reportName: 'Pytest HTML Report'
                    ])
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline completed - ${currentBuild.result}"
            // 可选：清理工作空间
            // cleanWs()
        }
        success {
            echo "✅ Pipeline succeeded!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}