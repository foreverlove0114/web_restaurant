pipeline {
    agent any

    triggers {
        // 1. Poll SCM 触发器 - 每30分钟检查一次
        pollSCM('H/30 * * * *')

        // 2. Generic Webhook Trigger
        genericTrigger(
            genericVariables: [
                [key: 'ref', value: '$.ref'],
                [key: 'repository_url', value: '$.repository.html_url']
            ],
            causeString: 'Triggered by $ref',
            token: 'WEBHOOK_TOKEN_12345', // 可选安全令牌
            printContributedVariables: true,
            printPostContent: true,
            silentResponse: false
        )
    }

    environment {
        BASE_URL = 'http://localhost:8000'
        PYTHON_PATH = 'C:\\Python313\\python.exe'  // 根据你的环境调整
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
                    // 保存测试报告
                    allure includeProperties: false,
                          jdk: '',
                          results: [[path: 'allure-results']]
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
                    # 例如: python app.py 或你的部署脚本
                    echo "Deployment completed!"
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline completed - ${currentBuild.result}"
            // 清理工作空间（可选）
            // cleanWs()
        }
        success {
            emailext (
                subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "测试通过，部署成功！\n检查报告: ${env.BUILD_URL}",
                to: "your-email@example.com"
            )
        }
        failure {
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "测试失败，请检查！\n详情: ${env.BUILD_URL}",
                to: "your-email@example.com"
            )
        }
    }
}