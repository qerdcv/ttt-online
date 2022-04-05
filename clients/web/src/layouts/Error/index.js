import styles from "layouts/Error/error.module.scss";

const defaultCodeMap = {
  404: "Not found",
  500: "Internal Server Error",
  401: "Not authorized"
}

export const Error = ({code=404, text}) => (
  <div className={styles.error}>
    <h1>
      <u className={styles.errorCode}><i>{code}</i></u><span className={styles.errorMessage}>{text || defaultCodeMap[code]}</span>
    </h1>
  </div>
)
