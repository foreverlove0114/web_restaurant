pipeline {
    agent any

    triggers {
        // 1. Poll SCM 触发器 - 每30分钟检查一次
        pollSCM('H/30 * * * *')

        // 2. Generic Webhook Trigger - 注意首字母大写
        GenericTrigger(
            genericVariables: [
                [key: 'ref', value: '$.ref'],
                [key: 'repository_url', value: '$.repository.html_url']
            ],
            causeString: 'Triggered by $ref',
            token: 'WEBHOOK_TOKEN_12345',
            printContributedVariables: true,
            printPostContent: true,
            silentResponse: false
        )
    }

    environment {
        BASE_URL = 'http://localhost:8000'
        PYTHON_PATH = 'C:\\Python313\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/foreverlove0114/web_restaurant.git',
                    credentialsId: ''  // 如果有认证，填写 credentialsId
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                    echo "Setting up Python environment..."
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install -r requirements.txt
                    pip install pytest allure-pytest pytest-html
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    echo "Running tests..."
                    pytest --alluredir=allure-results --html=pytest-report.html --self-contained-html
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

        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                bat '''
                    echo "Deploying application..."
                    call venv\\Scripts\\activate
                    # 这里添加你的部署命令
                    echo "Deployment completed!"
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline completed - ${currentBuild.result}"
        }
        success {
            echo "✅ Pipeline succeeded!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}